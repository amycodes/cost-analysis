import os, requests, json
import mysql.connector


def connect_db():
    config = {
        "user": os.getenv("MYSQL_BILLING_USER"),
        "password": os.getenv("MYSQL_BILLING_PASSWORD"),
        "host": os.getenv("MYSQL_BILLING_HOST"),
        "port": os.getenv("MYSQL_BILLING_PORT"),
        "database": "do-invoice",
        "ssl_ca": "billingdb.crt",
        "ssl_verify_cert": True,
    }

    return mysql.connector.connect(**config)


def disconnect_db(db):
    db.cursor().close()
    db.close()


def init_db(db=False, table="invoice_details"):
    if db:
        c = db.cursor()
        c.execute("Show tables;")
        all_tables = c.fetchall()
        # geeksforgeeks.org/how-to-show-all-tables-in-mysql-using-python

        has_table = False
        for t in all_tables:
            if table == t[0]:
                has_table = True
                break
        if has_table:
            q = "truncate {0}".format(table)
        else:
            q = "CREATE TABLE {0} (id INT AUTO_INCREMENT PRIMARY KEY, invoice_uuid varchar(64))".format(
                table
            )
        c.execute(q)


def test_db(db=False, table="invoice_details"):
    if db != False:
        c = db.cursor()
        print("describe {0}".format(table))
        c.execute("describe {0}".format(table))
        table_desc = c.fetchall()
        for col in table_desc:
            print(col[0])


def fetch_invoice(db=False, table="invoice_details"):
    status = "Loaded"
    key = "Bearer {0}".format(os.getenv("DO_APIKEY"))

    headers = {"Content-Type": "application/json", "Authorization": key}
    r = requests.get(
        "https://api.digitalocean.com/v2/customers/my/invoices", headers=headers
    )
    status = "Fetched Invoices"
    report = json.loads(r.text)
    if report["invoices"]:
        status = "Found {0} Invoices".format(len(report["invoices"]))
        columns = []
        if db != False:
            c = db.cursor()
            print("describe {0}".format(table))
            c.execute("describe {0}".format(table))
            table_desc = c.fetchall()
            for col in table_desc:
                columns.append(col[0])

        for i in report["invoices"]:
            invoice_url = (
                "https://api.digitalocean.com/v2/customers/my/invoices/{0}".format(
                    i["invoice_uuid"]
                )
            )
            print("Fetching from Invoice #{0}".format(i["invoice_uuid"]))
            ir = requests.get(invoice_url, headers=headers)
            invoice = json.loads(ir.text)
            if invoice["invoice_items"]:
                for item in invoice["invoice_items"]:
                    if db != False:
                        cols = ["invoice_uuid"]
                        vals = ["'{0}'".format(i["invoice_uuid"])]
                        for key in item.keys():
                            if key not in columns:
                                type = (
                                    "float"
                                    if key in ["amount", "duration"]
                                    else "varchar(64)"
                                )
                                q = "ALTER TABLE {0} ADD {1} {2}".format(
                                    table, key, type
                                )
                                db.cursor().execute(q)
                                columns.append(key)
                            cols.append(key)
                            if key in ["amount", "duration"]:
                                vals.append(item[key])
                            else:
                                vals.append("'{0}'".format(item[key]))
                        insert = "INSERT INTO {0} ({1}) VALUES ({2})".format(
                            table, ",".join(cols), ",".join(vals)
                        )
                        db.cursor().execute(insert)
                        db.commit()

                    else:
                        print(str(item.keys()))


db = connect_db()

init_db(db)
fetch_invoice(db)
disconnect_db(db)

print("---done--")
