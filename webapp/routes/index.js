const express = require('express')
const router = express.Router()
// Hold request timestamps per IP
const clientRequestTimestamps = {};
// Maximum number of requests per minute per client
const MAX_REQUESTS_PER_MINUTE = 25;
// Local Data - holds articles and tag list
const database = require('../data/articles.json')


// Used to get article from local json database
function get_article(action_string)
{
    // convert action string to int
    let action = parseInt(action_string)
    // Get the string value of action using index and passing into array of actions
    let action_str = database.tags[action]
    //console.log(`Selected action: ${action_str}`)
    // Filter out articles using the current action(tag) - 
    // this should be articles preferences by the user over times of liking similar articles with same tag
    let possible_articles = database.articles.filter(item =>item.tag ==action_str)

    // Randomly select an article out of the filtered articles to display
    const randomIndex = Math.floor(Math.random() * possible_articles.length);
    
    return possible_articles[randomIndex];
}

// Rate limiter for requests to avoid stress on server
const rateLimitMiddleware = (req, res, next) => {
    const clientIP = req.ip; // Use IP as identifier (you could also use a token)
    const now = Date.now();
    const timestamps = clientRequestTimestamps[clientIP] || [];
  
    // Remove timestamps older than one minute (60000 milliseconds)
    const recentTimestamps = timestamps.filter(ts => now - ts < 60000);
  
    // Check if the client has exceeded the rate limit
    if (recentTimestamps.length >= MAX_REQUESTS_PER_MINUTE) {
      res.status(429).json({msg:'Too many requests. Try again in a minute by refreshing page.'});

      return;
    }
  
    // Record the current timestamp for this client
    recentTimestamps.push(now);
    clientRequestTimestamps[clientIP] = recentTimestamps;
  
    // Continue processing the request
    next();
};

// Route to initialize new agent 
router.get('/', rateLimitMiddleware, async (req,res)=>{
    fetch('https://ml.jodadev.com/initialize')
    .then(response=>response.json())
    .then(data=>{
        // Render page with article data
        res.render('index', {recommended: get_article(data.action)})
    })
    .catch(err=>{
        console.log(`${err.message} - AI API {Recommendation}`)
        res.render('index')
    })
})

// Route to update AI with new data to learn
router.post('/learn', rateLimitMiddleware,(req,res)=>{
    // data to send with request to ML API
    const data = {
        action: req.body.tag, 
        // depending on button id, if like then we want to reward, else, don't
        reward: req.body.user_action == 'like' ? true : false
    }
  
    // send request to ML API  
    fetch('https://ml.jodadev.com/learn',{
        method: "POST",
        headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(data)
    })
    .then(response=>response.json())
    .then(res_data=>{
        if (res_data.Q)
        {
            // Gets the index of the max and min Q-Value in Q-Table
            max = res_data.Q.indexOf(Math.max(...res_data.Q))
            min = res_data.Q.indexOf(Math.min(...res_data.Q))

            res.status(200).json({
                Q: res_data.Q,
                selection_state: res_data.selection_state,
                alpha: res_data.alpha,
                epsilon: res_data.epsilon,
                // Get tag names using index from database
                max: database.tags[max],
                min: database.tags[min],
                recommended: get_article(res_data.action)
            })
        } 
    })
    .catch(err=>{
        console.log(err)
    })
})


module.exports = router