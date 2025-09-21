// Test the frontend API route
const frontendApiUrl = "http://localhost:3001/api/review-pr";

// Test data
const testData = {
  prUrl: "https://github.com/owner/repo/pull/123",
};

fetch(frontendApiUrl, {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
  },
  body: JSON.stringify(testData),
})
  .then((response) => {
    console.log(`Status Code: ${response.status}`);
    return response.text();
  })
  .then((data) => {
    console.log(`Response: ${data}`);
  })
  .catch((error) => {
    console.error(`Error: ${error}`);
  });
