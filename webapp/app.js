require('dotenv').config()
const path = require('path')
const express = require('express')
const app = express()
const Router = require('./routes/index')

app.use(express.static(path.resolve(__dirname,'public')))
app.use(express.json())
app.use(express.urlencoded({extended:false}))
app.use(Router)
app.set('view engine','pug')
app.set('views',path.resolve(__dirname,'views'))

module.exports = app;