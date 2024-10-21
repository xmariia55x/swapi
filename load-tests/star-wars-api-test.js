import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate } from 'k6/metrics';

// Declare the metric to stablish a success rate
const successRate = new Rate('successful_requests');

const BASE_URL = 'http://star-wars-api:5000';

export const options = {
  stages: [
    { duration: '30s', target: 10 },
    // { duration: '1m', target: 20 },
    { duration: '30s', target: 0 },
  ],
  thresholds: {
    successful_requests: ['rate>0.95'], // The minimun successfull requests must be a 95%
  },
};

export default function () {
  // Generate random values to request a different page number
  const page = Math.floor(Math.random() * 9) + 1; // Between 1 and 9 for "page"
  const all = Math.random() > 0.5 ? 'true' : 'false'; // Random boolean for "all"

  const url = `${BASE_URL}/people/data?page=${page}&all=${all}`;
  const res = http.get(url);

  // Check if the response status was 200
  const checkRes = check(res, {
    'status is 200': (r) => r.status === 200,
  });

  // Register the result
  successRate.add(checkRes);

  // Wait 1 second to perform the next request
  sleep(1);
}
