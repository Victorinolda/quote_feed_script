
#!/bin/bash

curl 'http://localhost:8004/api/v0/market/place-holder-id/cob-order/' \
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
  --data-raw '{"security_id":"841ac8c7-e921-4501-9bef-39f1f39c60ab","expiration":"0s","quantity":10000,"notional":"1000000","direction":"ask","order_type":"ioc","yield_value":"11.000"}'

