
#!/bin/bash


for i in {1..200}; do
    curl 'http://localhost:8004/api/v0/market/MX0MGO0000P2/cob-order/' \
      -H 'Accept: application/json' \
      -H 'Accept-Language: en-US,en;q=0.9' \
      -H 'Authorization: Token ba0b6c3bf2af73cc348a6842bdcebfef5e3b1e8f' \
      -H 'Connection: keep-alive' \
      -H 'Content-Type: application/json' \
      -H 'Origin: http://localhost:3000' \
      -H 'Referer: http://localhost:3000/' \
      -H 'Sec-Fetch-Dest: empty' \
      -H 'Sec-Fetch-Mode: cors' \
      -H 'Sec-Fetch-Site: same-site' \
      -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36' \
      -H 'X-CSRFToken: VYmHVerjy9mTfLpe9ALKYz9BR1X63wWKj26cqN9P8DaxSA6WaUAokJGd6Ms6KJLp' \
      -H 'sec-ch-ua: "Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"' \
      -H 'sec-ch-ua-mobile: ?0' \
      -H 'sec-ch-ua-platform: "macOS"' \
      --data-raw '{"security_id":"d1cc56db-150b-4cd5-9654-3aef92267f9b","security_name":"M Bono 7.750% May-2031","expiration":"2s","quantity":100000,"notional":"10000000","direction":"bid","order_type":"limit","yield_value":"11"}'
done
