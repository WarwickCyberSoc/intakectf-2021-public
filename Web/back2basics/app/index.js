const express = require("express");
const path = require("path");
const cookieParser = require("cookie-parser");

const app = express();
const port = process.env.PORT || 8080;

app.use("/static", express.static("static"));
app.use(cookieParser());

app.use((req, res, next) => {
  if (req.query.a && req.query.b) {
    try {
      const a = parseInt(req.query.a);
      const b = parseInt(req.query.b);

      if (a + b === 100) {
        return res.send("WMG{GeT_ParamS_ArE_AnYWhErE_AnD_EveryWherE}");
      } else {
        return res.send("Not quite! Make sure they add to 100!");
      }
    } catch {}
  }

  return next();
});

app.get("/", (req, res) => {
  if (req.cookies?.isAdmin === "1") {
    res.clearCookie("isAdmin").send("WMG{USeRs_ConTRol_ThE_CooKie_JaR}");
  } else {
    res.set("X-Flag", "WMG{HTtP_HeADErS_Can_SToRE_CReDenTiAls!1!}").cookie("isAdmin", "0").sendFile(path.join(__dirname, "/index.html"));
  }
});

app.post("/mail", express.text(), (req, res) => {
  if (req.body === "mail me the flag") {
    return res.send("WMG{PoST_Is_VeRY_HelPFuL_FoR_HtTp}");
  } else {
    return res.send("Unknown body! Try again! You'll need to include the 'Content-Type' header of 'text/plain'!");
  }
});

app.listen(port, () => {
  console.log(`CURL Intro: listening on ${port}`);
});
