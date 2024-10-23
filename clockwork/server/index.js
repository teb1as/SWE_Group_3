const express = require('express');
const app = express();
const cors = require('cors');

app.use(cors())


app.get('/', (req, res) => { //sends message to client side
    res.send('Server communucation!')
})

app.listen(5100, () => { //confirms server is functioning
    console.log('server listening on port 5100')
})
