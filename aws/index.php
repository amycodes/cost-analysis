<?php
    require_once __DIR__ . '/vendor/autoload.php';

    use Aws\CostExplorer;
        
    use MongoDB\Driver\ServerApi;
    use MongoDB\Client;
    use MongoDB\Driver\WriteConcern;
    
    $ce_client = new Aws\CostExplorer\CostExplorerClient([
        'profile' => 'default',
        'region' => 'us-west-2'
    ]);
    $end = new DateTimeImmutable();
    $interval = new DateInterval('P1M');
    $start = $end->sub($interval);
    $end_format = date_format($end, 'Y-m') . '-01';
    $start_format = date_format($start, 'Y-m') . '-01';

    $cur = $ce_client->getCostAndUsage([
        'Granularity' => 'DAILY', // REQUIRED
        'Metrics' => ['BLENDED_COST', 'UNBLENDED_COST', 'AMORTIZED_COST', 'NET_AMORTIZED_COST', 'NET_UNBLENDED_COST', 'USAGE_QUANTITY', 'NORMALIZED_USAGE_AMOUNT'], // REQUIRED
        'TimePeriod' => [ // REQUIRED
            'End' => $end_format, // REQUIRED
            'Start' => $start_format, // REQUIRED
        ],
        'GroupBy' => [
            [
                'Key' => 'SERVICE',
                'Type' => 'DIMENSION',
            ],
            [
                'Key' => 'USAGE_TYPE',
                'Type' => 'DIMENSION',
            ]
        ],
        ]
    );
        
    // Set the version of the Stable API on the client
    $apiVersion = new ServerApi(ServerApi::V1);
    // Create a new client and connect to the server
    $mongodb_client = new MongoDB\Client(getenv('MONGODB_URI'), [], ['serverApi' => $apiVersion]);
    try {
        $collection = $mongodb_client->aws_billing->billing_demo;
       $result = $collection->insertMany( $cur['ResultsByTime'] );
       printf("Inserted %d document(s)\n", $result->getInsertedCount());
       var_dump($result->getInsertedIds());
    } catch (Exception $e) {
        printf($e->getMessage());
    }

