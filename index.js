const postData = {
  input:
    "Can you give a linear approximation example and answer from the book. Provide the page number or chapter number",
  file: "https://firebasestorage.googleapis.com/v0/b/learnlink-87932.appspot.com/o/Calculus.pdf?alt=media&token=d916ee9d-ef04-4182-baef-ad31ef8b42a1",
  language: "English",
};

fetch("http://127.0.0.1:5000/", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
  },
  body: JSON.stringify(postData),
})
  .then((response) => response.json())
  .then((data) => {
    console.log("Response from server:", data);
  })
  .catch((error) => {
    console.error("Error:", error);
  });
