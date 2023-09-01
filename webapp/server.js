const app = require('./app.js')
const PORT = 3001
app.listen(PORT,(req,res)=>{
    console.log(`Listening on port ${PORT}`)
})