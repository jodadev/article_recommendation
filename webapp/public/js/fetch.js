// timer function to display when AI will be available again after a request limit is reached
function startCountdown(durationInSeconds) {
    let remainingTime = durationInSeconds;

    // Update the countdown every 1 second
    const intervalId = setInterval(() => {
      document.querySelector("#tag").innerHTML = remainingTime + ' seconds left';

      remainingTime--;

      if (remainingTime < 0) {
        clearInterval(intervalId);  // Stop the countdown
        document.querySelector("#tag").innerHTML = 'Ready to refresh page!';
      }
}, 1000)};


// add event listeners to the two buttons "Like" and "Ignore"
document.querySelectorAll('.user_input').forEach(el=>{
    el.addEventListener('click',user_button_input,false)
})

// Handle user input with button selection
function user_button_input(e)
{
    // Make an object to store data about user input
    const data = {
        tag: e.target.name, 
        user_action: e.target.id
    }
    
    // send information to server
    fetch('/learn',{
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        // Handle too many requests error
        if (response.status === 429)
        {
            // Remove button events and display
            document.querySelectorAll('.user_input').forEach(el=>{
                el.removeEventListener(el,user_button_input)
                el.style.display = 'none'
            })
            // Update text to info user
            document.querySelector('#title').innerHTML = 'Too many requests!'
            document.querySelector('#content').innerHTML = 'Please wait 1 minute and refresh the page. Note: a new agent will be created.'
            // Display a timer countdown for request limit reset
            startCountdown(60)
            return;
        }
        return response.json()
    })
    .then(res_data=>{
        if (res_data != undefined)
        {
            
            let result_wrapper = document.querySelector('#results')
            let content = `
                <h2>Q-Table</h2>
                <table>
                    <tr>
                        <th>Tech</th>
                        <th>News</th>
                        <th>Health</th>
                        <th>Money</th>
                    </tr>
                    <tr>
                        <td>${res_data.Q[0]}</td>
                        <td>${res_data.Q[1]}</td>
                        <td>${res_data.Q[2]}</td>
                        <td>${res_data.Q[3]}</td>
                    </tr>
                </table> 
                <p>The table above is the Agent's(AI) Q-Table which shows how confident the 
                agent is about what article the user prefers based on its tag. 
                The agent is always learning so this information is based on your current 
                action to "Like" or "Ignore" an article. The table shows 4 columns
                with a header, in order: "Tech", "News", "Health" and "Money". These stand
                for tags in which an article can belong to. The values below the header are the 
                Q-Values(Quality Values). The tag with the highest Q-Value is the preferred
                tag in which the agent will use to recommend articles.</p> 
                <p> <b>Note:</b> Even though a tag can have the highest Q-Value, other tags may still be 
                chosen if the agent decides on recommending something new(Exploration), else, the
                agent will usually go with what it knows(Exploitation).</p> 
                <h3>Conclusion (Time-Step)</h3>
                <ul>
                    <li>The agent is confident that articles using the tag, <b>"<u>${res_data.max}</u>"</b> should be recommended.</li>
                    <li>The agent is least confident in the tag, <b>"<u>${res_data.min}</u>"</b>.</li>
                    <li>The agent's action selection method<i>(method to choice a tag)</i> was selected in a state of <b><u>${res_data.selection_state}</u></b> </li>
                    <li>Learning Rate(alpha) is set to <u>${res_data.alpha}</u></li>
                    <li>Epsilon is set to <u>${res_data.epsilon}</u></li>
                </ul>   
            `
            // Update results
            result_wrapper.innerHTML = content
            // Update recommended
            document.querySelector('#title').innerHTML = res_data.recommended.title
            document.querySelector('#tag').innerHTML = 'Tag: "'+res_data.recommended.tag +'"'
            document.querySelector('#content').innerHTML = res_data.recommended.content
            // Update button names to ensure selection works
            document.querySelector('#like').name = res_data.recommended.tag
            document.querySelector('#ignore').name = res_data.recommended.tag
        }
        
    })
        
    // {
    //     // response should be a redirection, so update the location
    //     if (response.redirected) {
    //         window.location.href = response.url;
    //     }
    // })    
}