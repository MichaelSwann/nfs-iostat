const express = require('express');
const pg = require('pg');
const insert = require('./insert');

const pool = new pg.Pool({
  user: 'nfs_admin',
  host: 'localhost',
  database: 'nfsstats',
  password: 'Egh0noo9iey6IeZ',
  port: 5432,
});

const app = express();
app.use(express.json());

app.post('/nfs/api/save', (req, res) => {
  const stat = req.body;
  console.log(stat['server']);
  insert(stat, pool);
  res.sendStatus(200);
})


// make sure their is a connection to the database
// before listening
if (pool.err) {
  console.error('Error creating pool:', pool.err)
  process.exist(2)
} else {
  app.listen(3000)
}
