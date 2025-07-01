const express = require("express");
const safeFs = require("@opengovsg/starter-kitty-fs").default;
const fs = require("fs");
const allowedMethods = Object.keys(require("./node_modules/@opengovsg/starter-kitty-fs/dist/params.js").default);

const app = express();

app.use(express.json());


app.post("/", (req, res)=>{
    const basePath = fs.mkdtempSync("./sandbox/");
    (async ()=>{
        const {method, args} = req.body;
        if(typeof method !== "string" || !allowedMethods.includes(method)){
            return res.status(400).send("Invalid method");
        }

        const sandboxedFs = safeFs(basePath);

        if(args.some(arg=>typeof arg === "number")){
            // Please don't DoS my app by doing readfileSync(5) or something
            // Hopefully this check is sufficient...
            return res.status(400).send("Invalid argument");
        }

        const result = sandboxedFs[method](...args);

        res.status(200).send(JSON.stringify(result));

    })().catch(err=>{
        console.log("Error:", err);
        res.status(400).send("An error occurred!!");
    }).finally(()=>{
        fs.rmSync(basePath, {
            recursive: true,
            force: true
        })
    })
})

app.listen(3334)