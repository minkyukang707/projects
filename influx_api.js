const Influx = require('influx')
const express = require('express')
const http = require('http')
const os = require('os')

const app = express()

const influx = new Influx.InfluxDB({
    host: 'localhost',
    database: 'kdd',
    schema: [
      {
        measurement: 'networkintrusion',
        fields: {

        },
        tags: [
          'host'
        ]
      }
    ]
})

influx.getDatabaseNames()
.then(names => {
if (!names.includes('kdd')) {
    return influx.createDatabase('kdd');
}
})
.then(() => {
http.createServer(app).listen(8085, function () {
    console.log('Listening on port 8085')
})
})
.catch(err => {
console.error(`Error creating Influx database!`);
})

app.use((req, res, next) => {
const start = Date.now();

    res.on("finish", () => {
        const duration = Date.now() - start;
        console.log(`Request to ${req.path} took ${duration}ms`);

        influx
        .writePoints([
            {
            measurement: "networkintrusion",
            tags: { host: os.hostname() },
            fields: { duration, path: req.path },
            },
        ])
        .catch((err) => {
            console.error(`Error saving data to InfluxDB! ${err.stack}`);
        });
        });
        return next();
});

app.get("/all", function (req, res) {
    influx
      .query(
        `
      select * from networkintrusion
    `
      )
      .then((result) => {
        res.json(result);
      })
      .catch((err) => {
        res.status(500).send(err.stack);
      });
  });