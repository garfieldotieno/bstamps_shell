
let APP_PARENT_ELEMENT = document.querySelector('.parent_display_container');

window.addEventListener('DOMContentLoaded', function() {  
  refreshDisplay(); 
  setInitialZoom(); // Set the initial zoom level to 90% when the page loads

  // Select all elements with the class "itemForm"
  const itemForms = document.getElementsByClassName("itemForm");

  // Iterate over each element and attach the event listener
  Array.from(itemForms).forEach(function(itemForm) {
    itemForm.addEventListener("submit", function(event) {
      event.preventDefault(); // Prevent the default form submission behavior
    
      // Add your logic here if needed
    
      // For this example, we do nothing after preventing the default behavior
    });
  });
  
});


// Function to set the initial zoom level on page load
function setInitialZoom() {
  // console.log(`zooming`)
  const initialZoom = 0.8; // 80%
  document.documentElement.style.zoom = initialZoom;
}




function refreshDisplay(){
  render_ui();
}

function getScreenMode(){
  if (window.innerWidth > 777){
    return 'large';
  }
  else if (window.innerWidth <= 777){
    return 'small';
  }
}

// test function to print yup
function render_ui(){
  var startX = 0;
  window.scrollTo(startX, 0);

  if(getScreenMode() == 'small'){
    console.log('yup, small screen')
  }
  else if (getScreenMode() == 'large'){
    console.log('yup, large screen')
  }
  
}

// bot components section
function get_to_date_string(element_object){
  let d = new Date();
  const months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
  const days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];

  element_object.innerHTML=`<b>${days[d.getDay()]} ${d.getDate()} ${months[d.getMonth()]}</b>`

}

let bot_header_big = document.getElementById("bot_header_big");
get_to_date_string(bot_header_big)

let bot_header_small = document.getElementById("bot_header_small");
get_to_date_string(bot_header_small)

// Get the bot_app element
const botApp = document.querySelector('.bot_app');

// Get the initial offset from the top
const initialOffset = botApp.getBoundingClientRect().top;



// Function to update the position of bot_app for large screens
function updateBotAppPosition() {
  const screenMode = getScreenMode();
  if (screenMode === 'large') {
      const scrollTop = window.scrollY;
      const threshold = 4; // You can adjust this value
      // console.log(`scrollTop value : ${scrollTop}`)
      botApp.style.position = 'absolute';
      botApp.style.top = `${threshold}px`
    
  } 
}

// Add a scroll event listener to update the position during scrolling
window.addEventListener('scroll', updateBotAppPosition);

// Call the function on page load to set the initial position
updateBotAppPosition();

function show_small_bot_home(){
  // console.log('about to hide l_d_s and show bot_display_section_small')
  document.querySelector(".large_display_section").style.display = "none";
  document.querySelector(".bot_display_section_small").style.display = "block";
}

function upload_file(){
  console.log(`${this}`)
  let file_input_el = document.createElement('input');
  file_input_el.setAttribute('type', 'file');
  file_input_el.addEventListener('change', process_ticket_qr);
  file_input_el.click();
}

let scan_res_var = ""

function process_ticket_qr(event) {
  uploadedFile = event.target.files[0];
  // console.log(`uploaded file is : ${uploadedFile}`);
  generate_prompt_mode();
}


async function generate_prompt_mode() {
  console.log('prompt mode activated');

  let bot_container = document.querySelector('.bot_display_section');
  let bot_app = document.querySelector('.bot_app');
  let bot_input_section = document.querySelector('.bot_input_section');
  let button_stack = bot_app.children[3];
  console.log('Printing button_stack:');
  console.log(button_stack);

  button_stack.innerHTML = ''

  // Create the input field for redeem code
  let bot_input_redeem_code = document.createElement('input');
  bot_input_redeem_code.classList.add('bot_input_redeem_code');
  bot_input_redeem_code.type = 'text';
  bot_input_redeem_code.placeholder = 'REDEEM CODE';
  bot_input_redeem_code.name = 'redeem_code';

  bot_input_redeem_code.addEventListener('input', function(event) {
    const userInput = event.target.value;
    // console.log('User Input:', userInput);
    // Check if the .input-error class is present
    if (bot_input_redeem_code.classList.contains('input-error')) {
      bot_input_redeem_code.classList.remove('input-error');
    }
    // Additional actions based on the input value can be added here
  });



  bot_input_section.appendChild(bot_input_redeem_code);

  let buttonTemplate = `
    <div class="bot_button_layer">
        <button class="bot_button" onclick="CLICK_EVENT">
            <div class="row">
                <div class="col-8">
                    <span class="type-label">LABEL</span>
                </div>
                <div class="col-4">
                    <span class="type_label">
                        <i class="fa ICON_CLASS"></i>
                    </span>
                </div>
            </div>
        </button>
    </div>
`;


// Create the submit button
button_stack.innerHTML = button_stack.innerHTML + buttonTemplate.replace('CLICK_EVENT', 'process_submit()').replace('LABEL', 'Submit').replace('ICON_CLASS', 'fa-arrow-right');



// Create the cancel button
button_stack.innerHTML = button_stack.innerHTML + buttonTemplate.replace('CLICK_EVENT', 'process_cancel()').replace('LABEL', 'Cancel').replace('ICON_CLASS', 'fa-times');



}

function process_cancel() {
  console.log("called cancel event");
  sessionStorage.clear()
  let baseEndpoint = window.location.origin; // Assuming the base endpoint is the same as the current origin
  let specificEndpoint = '/'; // Replace with the specific path where you want to redirect
  let params = new URLSearchParams({ intent: 'Cancel' }).toString();
  let finalURL = `${baseEndpoint}${specificEndpoint}?${params}`;
  window.location.href = finalURL;
}

function process_reset_session() {
  console.log("called reset session event");
  sessionStorage.clear()
  window.location.href = "/logout";
}

function process_login(){
  console.log("calling process login")
  sessionStorage.clear()
  let baseEndpoint = window.location.origin; // Assuming the base endpoint is the same as the current origin
  let specificEndpoint = '/login'; // Replace with the specific path where you want to redirect
  let params = new URLSearchParams({ swap: 'Y' }).toString();
  let finalURL = `${baseEndpoint}${specificEndpoint}?${params}`;
  window.location.href = finalURL;
}



function process_submit(){
  console.log("called function submit")
  // Capture the input value before form submission
  let bot_input_redeem_code = document.querySelector('.bot_input_redeem_code')
  const userInputValue = bot_input_redeem_code.value;

  // Perform the form submission and attach the uploaded file
  const formData = new FormData();
  formData.append('file', uploadedFile);
  formData.append('userInput', userInputValue);

  const baseEndpoint = window.location.origin; // Assuming the base endpoint is the same as the current origin
  const specificEndpoint = '/recognize_artifact'; // Adjust this to match your specific endpoint path
  const endpointURL = `${baseEndpoint}${specificEndpoint}`;

  fetch(endpointURL, {
      method: 'POST',
      body: formData
  })
  .then(response => response.json())
  .then(data => {
      

      if (data.status != true) {
          // Trigger the animation for the specific error message
          let bot_input_redeem_code = document.querySelector('.bot_input_redeem_code');
          if (bot_input_redeem_code.classList.contains('input-error')) {
              bot_input_redeem_code.classList.remove('input-error');
          }
          bot_input_redeem_code.classList.add('input-error');
      }else
      {
        console.log('operation successfull')
        if (data.card_operation && data.card_operation.trim().toLowerCase() === "auth_reset_card") {
          // Handle response data
          console.log(`Received data:`, data);
          sessionStorage.setItem('authCode', data.auth_card_gen.new_code);
          sessionStorage.setItem('download_url', data.auth_card_gen.url);
      
          // Clear the bot input section
          let bot_app = document.querySelector('.bot_app');
          let bot_input_section = document.querySelector('.bot_input_section');
          let button_stack = bot_app.children[3];
      
          let codeMessage = `Your Authentication Card has been generated. <br> Your Code for this card is <strong>${data.auth_card_gen.new_code}</strong>.`;
      
          bot_input_section.innerHTML = codeMessage;
      
          let buttonTemplate = `
              <div class="bot_button_layer">
                  <button class="bot_button" onclick="CLICK_EVENT">
                      <div class="row">
                          <div class="col-8">
                              <span class="type-label">LABEL</span>
                          </div>
                          <div class="col-4">
                              <span class="type_label">
                                  <i class="fa ICON_CLASS"></i>
                              </span>
                          </div>
                      </div>
                  </button>
              </div>
          `;
      
          button_stack.innerHTML = '';
      
          // Create the Copy button
          button_stack.innerHTML += buttonTemplate.replace('CLICK_EVENT', 'process_copy()').replace('LABEL', 'Copy').replace('ICON_CLASS', 'fa-clone');
      
          
      }
      
        else if (data.card_operation && data.card_operation.trim().toLowerCase() === "auth_card") {
          
          // Handle response data
          console.log(`Received data:`, data);
          // sessionStorage.setItem('authCode', data.auth_card_gen.new_code);
          // sessionStorage.setItem('download_url', data.url)
          
          
          
          let bot_app = document.querySelector('.bot_app');
          let bot_input_section = document.querySelector('.bot_input_section');
          let button_stack = bot_app.children[3];
      
          
      
          bot_input_section.innerHTML = '';
          bot_input_section.innerHTML = "You're ready to login, continue with the buttons below";

          let buttonTemplate = `
              <div class="bot_button_layer">
                  <button class="bot_button" onclick="CLICK_EVENT">
                      <div class="row">
                          <div class="col-8">
                              <span class="type-label">LABEL</span>
                          </div>
                          <div class="col-4">
                              <span class="type_label">
                                  <i class="fa ICON_CLASS"></i>
                              </span>
                          </div>
                      </div>
                  </button>
              </div>
          `;
      
          button_stack.innerHTML = '';

          button_stack.innerHTML += buttonTemplate.replace('CLICK_EVENT', 'process_login()').replace('LABEL', 'Login').replace('ICON_CLASS', 'fa-sign-in');
      
          // Create the cancel button
          button_stack.innerHTML += buttonTemplate.replace('CLICK_EVENT', 'process_reset_session()').replace('LABEL', 'Cancel').replace('ICON_CLASS', 'fa-times');
        }
      

      }
      // Add your further handling logic for a successful response here

      
    

  })
  .catch(error => {
      console.error(error)
      let bot_input_redeem_code = document.querySelector('.bot_input_redeem_code');
      bot_input_redeem_code.classList.add('input-error');
  });
}





function process_copy() {
  console.log('processing copy');
  // Access the stored value from session storage
  const codeToCopy = sessionStorage.getItem('authCode');

  let bot_app = document.querySelector('.bot_app');
  let button_stack = bot_app.children[3];

  let copy_clicked = sessionStorage.getItem('copy_clicked');

  let buttonTemplate = `
            <div class="bot_button_layer">
                <button class="bot_button" onclick="CLICK_EVENT">
                    <div class="row">
                        <div class="col-8">
                            <span class="type-label">LABEL</span>
                        </div>
                        <div class="col-4">
                            <span class="type_label">
                                <i class="fa ICON_CLASS"></i>
                            </span>
                        </div>
                    </div>
                </button>
            </div>
        `;

  if (!copy_clicked && codeToCopy) {
      // Create a temporary input element
      const tempInput = document.createElement('input');
      tempInput.value = codeToCopy;
      document.body.appendChild(tempInput);

      // Select the text
      tempInput.select();
      tempInput.setSelectionRange(0, 99999); // For mobile devices

      // Copy the text
      document.execCommand('copy');

      // Remove the temporary input
      document.body.removeChild(tempInput);

      console.log(`Copied the code: ${codeToCopy}`);

      sessionStorage.setItem('copy_clicked', 'true');
      button_stack.innerHTML += buttonTemplate.replace('CLICK_EVENT', 'process_download()').replace('LABEL', 'Download').replace('ICON_CLASS', 'fa-download');
  } else if (!copy_clicked) {
      console.error('Data is not available or does not have the required structure.');
  }
}

// Function for handling the download process
function process_download() {
  console.log('processing download');

  let bot_app = document.querySelector('.bot_app');
  let button_stack = bot_app.children[3];
  let bot_input_section = document.querySelector('.bot_input_section');
  bot_input_section.innerHTML = "You're ready to login, continue with the buttons below";

  let download_clicked = sessionStorage.getItem('download_clicked');

  if (!download_clicked) {
      
      let buttonTemplate = `
          <div class="bot_button_layer">
              <button class="bot_button" onclick="CLICK_EVENT">
                  <div class="row">
                      <div class="col-8">
                          <span class="type-label">LABEL</span>
                      </div>
                      <div class="col-4">
                          <span class="type_label">
                              <i class="fa ICON_CLASS"></i>
                          </span>
                      </div>
                  </div>
              </button>
          </div>
      `;

      // Create the Login button
      button_stack.innerHTML += buttonTemplate.replace('CLICK_EVENT', 'process_login()').replace('LABEL', 'Login').replace('ICON_CLASS', 'fa-sign-in');

      // Create the Cancel button
      button_stack.innerHTML += buttonTemplate.replace('CLICK_EVENT', 'process_reset_session()').replace('LABEL', 'Cancel').replace('ICON_CLASS', 'fa-times');

      sessionStorage.setItem('download_clicked', 'true');
  }

  let downloadURL = sessionStorage.getItem('download_url');
  // Check if the download URL exists
  if (downloadURL) {
      // Extract the URL path from the data
      const urlPath = downloadURL.split('/static')[1];
      // Create the complete download URL
      const completeDownloadURL = window.location.origin + '/static' + urlPath;
      // Create a new anchor element
      const link = document.createElement('a');
      link.href = completeDownloadURL;
      link.download = 'file_name'; // Set the desired file name here
      // Simulate click on the link to trigger the download
      link.click();
      // Remove the link from the DOM
      link.remove();
  } else {
      console.error('Download URL not found.');
  }
}







