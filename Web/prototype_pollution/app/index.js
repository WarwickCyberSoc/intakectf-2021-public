const express = require("express");
const app = express();
const port = 3000;
const _ = require("lodash");

const users = new Map();

app.use(express.json());

app.get("/", (req, res) => {
  res.send("Please give your <strike>personal data</strike> required data to POST /register\n");
});

app.post("/register", (req, res) => {
  const { username, password, name, birthday } = req.body;
  if (!username || !password || !name || !birthday)
    return res.status(400).json({ message: "You must include a username, password, name and birthday!" });

  if (users.has(username)) return res.status(400).json({ message: "A user already exists with this name" });

  const user = {
    password: password.toString(),
    name: name.toString(),
    birthday: birthday.toString(),
  };

  users.set(username, user);
  res.json({ message: "Account created!" });
});

app.patch("/update", (req, res) => {
  if ("isAdmin" in req.body) return res.status(400).json({ message: "You cannot make yourself an admin!!!" });

  const { username, password } = req.body;
  if (!username || !password) return res.status(400).json({ message: "You are not authenticated!" });

  const user = users.get(username);
  if (!user || user.password !== password) return res.status(400).json({ message: "You are not authenticated!" });

  users.set(username, _.merge(user, req.body));

  res.json({ message: "You have updated your profile." });
});

app.get("/flag", (req, res) => {
  const { username, password } = req.body;
  if (!username || !password) return res.status(400).json({ message: "You are not authenticated!" });

  const user = users.get(username);
  if (!user || user.password !== password || !user.isAdmin) return res.status(400).json({ message: "You are not authenticated!" });

  res.sendFile(__dirname + "/flag.txt");
});

app.listen(port, () => {
  console.log(`Listening at http://localhost:${port}`);
});
