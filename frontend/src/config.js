
// config.js
const API_BASE =
  (typeof process !== "undefined" &&
   process.env &&
   process.env.REACT_APP_PROJECT_API_BASE) ||
  (typeof window !== "undefined" && window.PROJECT_API_BASE) ||
  "http://localhost:5002"; // fallback if nothing else is set

export default API_BASE;
console.log("API_BASE =", API_BASE);