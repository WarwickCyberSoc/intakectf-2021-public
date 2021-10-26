const express = require("express");
const path = require("path");
const bodyParser = require("body-parser");

const app = express();
const port = process.env.PORT || 8080;

const flagPart1 = "WMG{CuRl_Is_SupER";
const flagPart2 = "_UsEFul_In_CTfS}";

app.use("/static", express.static("static"));
app.use(express.json());

app.get("/", (req, res) => {
  const userAgent = req.header("User-Agent") ?? "";
  if (userAgent.includes("curl")) {
    res.send(
      `You found the secret page for those who love curl :-) Here's half your flag!

${flagPart1}

Send a POST request to / with the JSON data '{"hello": "world"}' to get the second half!
`
    );
  } else {
    res.sendFile(path.join(__dirname, "/index.html"));
  }
});

app.post("/", (req, res) => {
  const userAgent = req.header("User-Agent") ?? "";
  if (userAgent.includes("curl")) {
    if (req.body.hasOwnProperty("hello") && req.body.hello === "world") {
      res.send(
        `Nice! Here's the rest of the flag.
      
${flagPart2}
`
      );
    } else {
      res.send("Not quite! Double check your POST request data! Make sure you include the correct Content-Type header!\n");
    }
  } else {
    res.sendFile(path.join(__dirname, "/index.html"));
  }
});

app.listen(port, () => {
  console.log(`CURL Intro: listening on ${port}`);
});
