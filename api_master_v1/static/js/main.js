
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


  let botHeader = document.getElementById("botHeader");
  

  get_to_date_string(botHeader);

  // Call the function to check and display storage mechanisms
  // checkAndDisplayStorageMechanisms();
    
});


// Function to set the initial zoom level on page load
function setInitialZoom() {
  // console.log(`zooming`)
  const initialZoom = 0.7; // 80%
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
function render_ui() {
  const error_data = "Function: render_ui"; // For error reporting
  var startX = 0;
  window.scrollTo(startX, 0);

  // Handle first-time contact with error handling
  try {
    handleFirstTimeContact();
  } catch (error) {
      showCriticalConsoleError(`${error.message} | ${error_data}`);
      console.error("Part A Error in handleFirstTimeContact:", error);
  }

  // Determine and handle screen mode with error handling
  try {
      const screenMode = getScreenMode();
      console.log('Screen mode:', screenMode);

      if (screenMode === 'small') {
          show_big_screen_context_btns();
      } else if (screenMode === 'large') {
          show_big_screen_context_btns();
      }
  } catch (error) {
      showCriticalConsoleError(`${error.message} | ${error_data}`);
      console.error("Part B Error in determining screen mode or executing related logic:", error);
  }
}



// bot components section
function get_to_date_string(element_object){
  console.log("calling get_to_date_string")
  let d = new Date();
  const months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
  const days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];

  element_object.innerHTML=`<b>${days[d.getDay()]} ${d.getDate()} ${months[d.getMonth()]}</b>`

}

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



// button functions

function process_button_master(button) {
  console.log('process button master');
  const select_btn = button.id;
  console.log(`selected button is ${select_btn}`);

  // Use a switch statement to handle button-specific logic
  switch (select_btn) {
    case "check_in":
      process_checkin();
      break;
    case "shop":
      process_shop();
      break;
    case "update_location":
      process_loca();
      break;
    case "proceed_shopping":
      process_proceed_shopping();
      break;
    case "wallet":
      process_wallet();
      break;
    case "refresh":
      process_refresh();
      break;
    case "camera":
      process_camera();
      break;
    case "take_photo":
      process_capture();
      break;
    case "qr_link":
      process_copy();
      break;
    case "call":
      process_call();
      break;
    case "mail":
      process_mail();
      break;
    case "about":
      process_about();
      break;
    case "base_cancel":
      process_base_cancel();
      break;
    case "second_cancel":
      process_second_cancel();
      break;
    case "redeem":
      process_checkin_redeem();
      break;
    case "purchase":
      process_checkin_purchase();
      break;
    case "checkin_redeem_copy":
      pasteRedeemCodeToInput()
      break;
    case "checkin_purchase_copy":
      pastePurchaseCodeInput()
      break;
    case "checkin_redeem_clear":
      clear_redeem_paste();
      break;
    case "checkin_purchase_clear":
      clear_purchase_paste();
      break;
    case "checkin_redeem_submit":
      process_checkin_redeem_submit();
      break;
    case "done":
      process_second_cancel();
      break;
    case "checkin_purchase_submit":
      process_checkin_purchase_submit();
      break;
    case "games":
      process_game();
      break;
    case "free_games":
      process_show_free_games();
      break;
    case "exit_gba":
      process_exit_gba();
      break;

    default:
      console.log(`No handler for button ID: ${select_btn}`);
  }
}


function process_base_cancel(){
  console.log('processing base_cancel');
  // ensure screen remains black
  document.getElementById("botScreenBig").src = botView.current_bot_screen_media[1];

  // time
  let botHeader = document.getElementById("botHeader");
  

  get_to_date_string(botHeader);

  // hide info div
  const botInfoDisplay = document.getElementById('botInfoDisplay');
  if (botInfoDisplay){
    botInfoDisplay.innerHTML='';
    botInfoDisplay.style.display = "none";

  }
  // hide nav giv
  const botNavigation = document.getElementById("botNavigation");
  if (botNavigation){
    botNavigation.innerHTML='';
    botNavigation.style.display = "none"
  }

  // restore start view
  const botButtonStackBig = document.getElementById("botButtonStackBig");
  botButtonStackBig.style.display = "block";

  const botButtonStackMiddle = document.getElementById("botButtonStackMiddle");
  botButtonStackMiddle.style.display = "block";

  const botButtonStackContact = document.getElementById("botButtonStackContact");
  botButtonStackContact.style.display = "block";

  if (html5QrCode){
    html5QrCode.stop().then((ignore) => {
      // QR Code scanning is stopped.
    }).catch((err) => {
      // Stop failed, handle it.
    });
  }

}

function process_second_cancel(){
  console.log('process second_cancel');

  document.getElementById('botScreenBig').src = botView.current_bot_screen_media[1];

  let botHeader = document.getElementById("botHeader");
  

  get_to_date_string(botHeader);
  
  const botInfoDisplay = document.getElementById('botInfoDisplay');
  if (botInfoDisplay){
    botInfoDisplay.innerHTML='';
    botInfoDisplay.style.display = "none";

  }

  // hide nav giv
  const botNavigation = document.getElementById("botNavigation");
  if (botNavigation){
    botNavigation.innerHTML='';
    botNavigation.style.display = "none"
  }

  // restore start view
  const botButtonStackBig = document.getElementById("botButtonStackBig");
  botButtonStackBig.style.display = "block";

  const botButtonStackMiddle = document.getElementById("botButtonStackMiddle");
  botButtonStackMiddle.style.display = "block";

  const botButtonStackContact = document.getElementById("botButtonStackContact");
  botButtonStackContact.style.display = "block";
  
}

function process_checkin(){
  console.log('process checkin');
  fold_bot_start_display();
  show_checkin_info();
  show_checkin_base_navigation();
}

function process_shop(){
  console.log('process shop');
  fold_bot_start_display();
  show_shop_base_0_info();
  show_shop_base_0_navigation();
}





// Function to animate the location button
function animate_location() {
  const location_btn = document.getElementById('update_location');
  if (location_btn) {
    // Trigger animations with staggered timing
    pulse(1000);
    pulse(3000);
    pulse(4000);
  }
}

function pulse(duration) {
  setTimeout(() => {
    const location_button = document.getElementById('update_location');
    if (location_button) {
      // Toggle the class between "bot_button" and "bot_button_reverse"
      if (location_button.className === "bot_button") {
        location_button.className = "bot_button_reverse";
      } else {
        location_button.className = "bot_button";
      }
    }
  }, duration);
}



// Function to stop location tracking and animate the button


var loca_stack = []; // To store location updates
var watchId = null; // To store the location watch ID


function quit_location_track() {
  const location_btn = document.getElementById('update_location');
  if (watchId) {
    // Stop watching location
    navigator.geolocation.clearWatch(watchId);
    watchId = null;
    console.log("Location tracking stopped.");

    // Log the final state of loca_stack
    console.log("Final Location Stack:", loca_stack);

    // Animate the location button to indicate stopping
    if (location_btn) {
      location_btn.className = "bot_button_stop"; // Add a class to visually indicate "stopped"
      setTimeout(() => {
        location_btn.className = "bot_button"; // Reset to the original class after the animation
      }, 2000); // Duration for the "stopping" animation
    }
  } else {
    console.log("No active location tracking to stop.");
  }
}
function process_loca() {
  console.log('processing loca');

  // Fetch the current location and update the display
  navigator.geolocation.getCurrentPosition(
    function (position) {
      animate_location(); // Animate when the location is fetched

      const botInfoDisplay = document.getElementById("botInfoDisplay");
      if (botInfoDisplay) {
        // Update the first child (h5) with "Updated Location"
        const h5Element = botInfoDisplay.querySelector("h5");
        if (h5Element) {
          h5Element.innerHTML = "Updated Location";
        }

        // Update the second child (p) with fetched coordinates
        const pElement = botInfoDisplay.querySelector("p");
        if (pElement) {
          const { latitude, longitude } = position.coords;
          pElement.innerHTML = `Fetched Coordinates: ${latitude}, ${longitude}`;

          // Push the coordinates to loca_stack
          loca_stack.push({ latitude, longitude });
          console.log('Current location stack is:', loca_stack);

          const botNavigation = document.getElementById("botNavigation");

          if (botNavigation) {
            const buttonElements = botNavigation.querySelectorAll("button"); // Get all button elements inside botNavigation
          
            // Check if there are exactly 2 button elements
            if (buttonElements.length === 2) {
              console.log("Bot navigation contains 2 buttons. Showing shop base navigation...");
          
              // Remove the last child element (last button) of botNavigation
              botNavigation.removeChild(botNavigation.lastElementChild);
          
              show_shop_base_1_navigation(); // Call the function to show shop base navigation
            } else if (buttonElements.length > 2) {
              console.log("Bot navigation contains more than 2 buttons. Passing...");
              // Do nothing if there are more than 2 buttons
            } else {
              console.log("Bot navigation contains less than 2 buttons.");
            }
          } else {
            console.error("Element with id 'botNavigation' not found.");
          }
          
          
        }
      }
    },
    function (error) {
      // Handle errors when the user cancels the location request or it fails
      console.error("Error fetching location:", error.message);

      const botInfoDisplay = document.getElementById("botInfoDisplay");
      if (botInfoDisplay) {
        const h5Element = botInfoDisplay.querySelector("h5");
        if (h5Element) {
          h5Element.innerHTML = "Location Access Denied";
        }

        const pElement = botInfoDisplay.querySelector("p");
        if (pElement) {
          pElement.innerHTML = "Please enable location access to fetch coordinates.";
        }
      }
    }
  );

  // Watch the location and update the display on change
  watchId = navigator.geolocation.watchPosition(
    function (position) {
      animate_location(); // Animate when the location is updated

      const botInfoDisplay = document.getElementById("botInfoDisplay");
      if (botInfoDisplay) {
        // Update the second child (p) with the updated coordinates
        const pElement = botInfoDisplay.querySelector("p");
        if (pElement) {
          const { latitude, longitude } = position.coords;
          pElement.innerHTML = `Updated Coordinates: ${latitude}, ${longitude}`;

          // Push the updated coordinates to loca_stack
          loca_stack.push({ latitude, longitude });
          console.log("Updated Location Stack:", loca_stack);
        }
      }
    },
    function (error) {
      // Handle errors when the location tracking fails or is canceled
      console.error("Error watching location:", error.message);

      const botInfoDisplay = document.getElementById("botInfoDisplay");
      if (botInfoDisplay) {
        const h5Element = botInfoDisplay.querySelector("h5");
        if (h5Element) {
          h5Element.innerHTML = "Location Tracking Error";
        }

        const pElement = botInfoDisplay.querySelector("p");
        if (pElement) {
          pElement.innerHTML = "Unable to track location updates. Please check permissions.";
        }
      }
    }
  );

  // Add event listener for the "update_location" button to stop location tracking
  document.getElementById('update_location').addEventListener('click', function () {
    quit_location_track(); // Stop location tracking and animate
  });

}


function process_proceed_shopping(){
  console.log('calling process_proceed_shopping');
  pr_status = check_pr_activated()

  if(pr_status == true){
    show_pu_pr_base();
  }
  else{
    show_pu_base();
  }

}

function show_pu_pr_base(){
  console.log('calling show_pu_pr_base');
  fold_bot_start_display();
  show_pu_pr_info();
  show_pu_pr_navigation();

}

function show_pu_base(){
  console.log('caling show_pu_base');
  fold_bot_start_display();
  show_pu_info();
  show_pu_navigation();

}

function process_wallet(){
  console.log('process wallet');
  fold_bot_start_display();
  show_wallet_info();
  show_wallet_base_navigation();
}


function process_camera(){
  console.log('process camera');
  fold_bot_start_display();
  show_scanner_info();
  show_scanner_base_navigation();
}



function process_capture() {
  console.log('calling process_capture');
  show_camera_screen();
  show_camera_screen_navigation();

  Html5Qrcode.getCameras()
    .then(devices => {
      if (devices && devices.length) {
        var cameraId = devices[1].id; // Use the first camera available
        const html5QrCode = new Html5Qrcode("reader"); // "reader" is the div where the stream will display

        // Start the camera feed and QR code scanning
        html5QrCode
          .start(
            cameraId,
            {
              fps: 10, // Optional, frame per seconds for QR code scanning
              qrbox: { width: 250, height: 250 } // Optional, bounding box for scanning UI
            },
            (decodedText, decodedResult) => {
              // Handle successful QR code scan
              console.log(`decodedText is ${decodedText}, and decodedResult is ${decodedResult}`);

              const botInfoDisplay = document.getElementById('botInfoDisplay');
              
              if (botInfoDisplay) {
                botInfoDisplay.innerHTML = `
                  <h5 class="bot_header">Scanned Code</h5>
                  <p class="bot_header">${decodedText}</p>
                `;

                const botNavigation = document.getElementById('botNavigation');

                if (botNavigation) {
                  const buttonBig = document.createElement('div');
                  buttonBig.classList.add('bot_button_layer');
                
                  const button = {};
                  button.id = "qr_link";
                  button.label = "Copy";
                  button.icon = "fa-solid fa-paste";
                
                  buttonBig.innerHTML = `
                    <button class="bot_button" id="${button.id}" onclick="process_button_master(this)">
                      <div class="row">
                        <div class="col-8">
                          <span class="type-label">${button.label}</span>
                        </div>
                        <div class="col-4">
                          <span class="type_label"><i class="${button.icon}"></i></span>
                        </div>
                      </div>
                    </button>
                  `;
                
                  if (botNavigation.firstChild) {
                    botNavigation.insertBefore(buttonBig, botNavigation.firstChild);
                  } else {
                    // If no child exists, simply append the new buttonBig
                    botNavigation.appendChild(buttonBig);
                  }
                }
                
              }

              // Stop the QR code scanning after a successful scan
              html5QrCode.stop().then(() => {
                console.log('QR code scanning stopped');
              }).catch(err => {
                console.error('Failed to stop scanning', err);
              });
            },
            (errorMessage) => {
              // Handle scan errors (e.g., no QR code in frame)
              console.log(`Scan error: ${errorMessage}`);
            }
          )
          .catch(err => {
            // Handle errors when starting the camera feed or scanning
            console.error('Error starting Html5Qrcode', err);

            const botInfoDisplay = document.getElementById('botInfoDisplay');
            if (botInfoDisplay) {
              botInfoDisplay.innerHTML = `
                <h5 class="bot_header">Error</h5>
                <p class="bot_header">${err}</p>
              `;
            }
          });
      }
    })
    .catch(err => {
      console.error('Unable to query camera information', err);
    });
}

function process_copy() {
  console.log('calling process_copy');

  // Get the botInfoDisplay element
  const botInfoDisplay = document.getElementById('botInfoDisplay');

  if (botInfoDisplay) {
    // Retrieve the second child of botInfoDisplay
    const secondElement = botInfoDisplay.children[1];

    if (secondElement) {
      // Get the innerHTML or text content of the second element
      const elValue = secondElement.innerHTML || secondElement.textContent;
      console.log('Value to copy:', elValue);

      // Copy the value to the clipboard
      navigator.clipboard.writeText(elValue)
        .then(() => {
          console.log('Copied to clipboard successfully!');
        })
        .catch(err => {
          console.error('Failed to copy to clipboard', err);
        });
    } else {
      console.error('Second child not found in botInfoDisplay');
    }
  } else {
    console.error('botInfoDisplay element not found');
  }
}


function process_about(){
  console.log('process about');
  fold_bot_start_display();
  show_about_info();
  show_about_base_navigation();
}


function process_refresh(){
  console.log('process refresh')
}


function process_call(){
  console.log('process call');
  // prompt call from device
  // Assuming you want to initiate a phone call, you can use the `tel:` protocol to prompt a call on mobile devices
  const phoneNumber = "254703103960"; // Example phone number, replace with dynamic data if needed
  window.location.href = `tel:${phoneNumber}`; // This will prompt the device to make a call to the provided number
}

function process_mail(){
  console.log('process mail');
  // prompt mail from device
  const subject = "Reach from Customer";
  const body = "Body content goes here";
  const recipient = "otienot75@gmail.com"; // Fixed recipient email address

  // Use the mailto protocol to open the default email client with the recipient, subject, and body
  window.location.href = `mailto:${recipient}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
  // This will open the default email client with the provided subject, body, and recipient email address pre-filled.
}

// checkin redeem

function process_checkin_redeem(){
  console.log('process checkin redeem option')

  fold_bot_start_display();
  const botInfoDisplay = document.getElementById('botInfoDisplay');
  if (botInfoDisplay){
    botInfoDisplay.innerHTML='';
    
  }
  // hide nav giv
  const botNavigation = document.getElementById("botNavigation");
  if (botNavigation){
    botNavigation.innerHTML='';
    
  }
  show_checkin_redeem_info();
  show_checkin_redeem_navigation();
}


function process_checkin_purchase(){
  console.log('process checkin purchase option')

  fold_bot_start_display();
  const botInfoDisplay = document.getElementById('botInfoDisplay');
  if (botInfoDisplay){
    botInfoDisplay.innerHTML='';
    
  }
  // hide nav giv
  const botNavigation = document.getElementById("botNavigation");
  if (botNavigation){
    botNavigation.innerHTML='';
    
  }

  show_checkin_purchase_info();
  show_checkin_purchase_navigation();

}

function process_checkin_redeem_submit(){
  console.log('calling process_checkin_redeem_submit, default success')

  fold_bot_start_display();

  const botInfoDisplay = document.getElementById('botInfoDisplay');
  if (botInfoDisplay){
    botInfoDisplay.innerHTML='';
    
  }
  // hide nav giv
  const botNavigation = document.getElementById("botNavigation");
  if (botNavigation){
    botNavigation.innerHTML='';
    
  }

  show_checkin_redeem_success_status_info();
  show_checkin_redeem_success_navigation();


}

function process_checkin_purchase_submit(){
  console.log('calling process_checkin_purchase_submit, default success');

  fold_bot_start_display();

  const botInfoDisplay = document.getElementById('botInfoDisplay');
  if (botInfoDisplay){
    botInfoDisplay.innerHTML='';
    
  }
  // hide nav giv
  const botNavigation = document.getElementById("botNavigation");
  if (botNavigation){
    botNavigation.innerHTML='';
    
  }

  show_checkin_purchase_success_status_info();
  show_checkin_purchase_success_navigation()

}

function process_game(){
  console.log('processing game');

  show_game_boy_advance_display()
  show_game_boy_advance_button_stack()


}

function process_exit_gba(){
  console.log('calling process_exit_gba');

  document.getElementById('botScreenBig').src = botView.current_bot_screen_media[1];

  let botHeader = document.getElementById("botHeader");
  

  get_to_date_string(botHeader);

  const botInfoDisplay = document.getElementById('botInfoDisplay');
  if (botInfoDisplay){
    botInfoDisplay.innerHTML='';
    botInfoDisplay.style.display = "none";
  }

  // hide nav giv
  const botNavigation = document.getElementById("botNavigation");
  if (botNavigation){
    botNavigation.innerHTML='';
    botNavigation.style.display = "none"
  }

  // restore start view
  const botButtonStackBig = document.getElementById("botButtonStackBig");
  botButtonStackBig.style.display = "block";

  const botButtonStackMiddle = document.getElementById("botButtonStackMiddle");
  botButtonStackMiddle.style.display = "block";

  const botButtonStackContact = document.getElementById("botButtonStackContact");
  botButtonStackContact.style.display = "block";

  // remove new_bot_section
  const botGBATopButtonStack = document.getElementById("botGBATopButtonStack")
  botGBATopButtonStack.style.display = "none"

  const botGBAMiddleButtonStack = document.getElementById("botGBAMiddleButtonStack")
  botGBAMiddleButtonStack.style.display = "none"

  const botGBAFooterButtonStack = document.getElementById("botGBAFooterButtonStack")
  botGBAFooterButtonStack.style.display = "none"
  
}

// minima stuff
// MDS.init(function(msg) {
//   try{
//     switch (msg.event) {
//       case "inited":
//           MDS.log("MDS has been initialised.");
//           break;
//       case "NEWBALANCE":
//           MDS.log("New balance: " + JSON.stringify(msg.data));
//           break;
//       case "NEWBLOCK":
//           MDS.log("New block: " + JSON.stringify(msg.data));
//           break;
//       case "MINING":
//           MDS.log("Mining status: " + JSON.stringify(msg.data));
//           break;
//       case "MINIMALOG":
//           MDS.log("Log message: " + JSON.stringify(msg.data));
//           break;
//       case "MAXIMA":
//           MDS.log("Maxima message: " + JSON.stringify(msg.data));
//           break;
//       case "MDS_TIMER_1HOUR":
//           MDS.log("One-hour timer event.");
//           break;
//       case "MDS_TIMER_10SECONDS":
//           MDS.log("10-second timer event.");
//           MDS.notify("This is a notification message.");
//           MDS.notifycancel();
//           break;
//       case "MDS_SHUTDOWN":
//           MDS.log("System shutdown message received.");
//           break;
//     }
//   }
//   catch(error){
//     console.log('error during mds init, ')
//     showCriticalConsoleError(`MDS init error ${error}`)
//   }
 
// });


function openDatabase() {
  return new Promise((resolve, reject) => {
      const request = indexedDB.open('SessionDatabase', 1);

      request.onupgradeneeded = (event) => {
          const db = event.target.result;
          console.log('Upgrading database...');
          if (!db.objectStoreNames.contains('sessions')) {
              db.createObjectStore('sessions', { keyPath: 'id' });
              console.log("Object store 'sessions' created.");
          }
      };

      request.onsuccess = (event) => {
          console.log('Database opened successfully.');
          const db = event.target.result;
          console.log('Object stores available:', db.objectStoreNames);
          resolve(db);
      };

      request.onerror = (event) => {
          console.error('Error opening database:', event.target.error);
          reject(event.target.error);
      };
  });
}

function persist(key, sessionObj) {
  openDatabase()
      .then((db) => {
          if (!db.objectStoreNames.contains('sessions')) {
              console.error("Object store 'sessions' does not exist!");
              return;
          }

          const transaction = db.transaction('sessions', 'readwrite');
          const store = transaction.objectStore('sessions');
          store.put(sessionObj);

          transaction.oncomplete = () => {
              console.log(`Session saved for key: ${key}`);
          };

          transaction.onerror = (event) => {
              console.error('Error saving session to IndexedDB:', event.target.error);
          };
      })
      .catch((error) => {
          console.error('Error opening database:', error);
      });
}

function clearDatabase() {
  return new Promise((resolve, reject) => {
      const request = indexedDB.open('SessionDatabase', 1);

      request.onsuccess = (event) => {
          const db = event.target.result;
          const transaction = db.transaction('sessions', 'readwrite');
          const store = transaction.objectStore('sessions');
          const clearRequest = store.clear();

          clearRequest.onsuccess = () => {
              console.log('Database cleared successfully.');
              resolve();
          };

          clearRequest.onerror = (event) => {
              console.error('Error clearing database:', event.target.error);
              reject(event.target.error);
          };
      };

      request.onerror = (event) => {
          console.error('Error opening database:', event.target.error);
          reject(event.target.error);
      };
  });
}


// Utility function to get a session by key
function getSession(key) {
  return new Promise((resolve, reject) => {
      openDatabase()
          .then((db) => {
              const transaction = db.transaction('sessions', 'readonly');
              const store = transaction.objectStore('sessions');
              const request = store.get(key);

              request.onsuccess = (event) => {
                  resolve(event.target.result);
              };

              request.onerror = (event) => {
                  reject(event.target.error);
              };
          })
          .catch((error) => {
              reject(error);
          });
  });
}

// Utility function to delete a session by key
function deleteSession(key) {
  openDatabase()
      .then((db) => {
          const transaction = db.transaction('sessions', 'readwrite');
          const store = transaction.objectStore('sessions');
          store.delete(key);
      })
      .catch((error) => {
          console.error('Error deleting session from IndexedDB:', error);
      });
}


// Utility function to get all sessions
function getCurrentSession() {
  return new Promise((resolve, reject) => {
    openDatabase()
      .then((db) => {
        const transaction = db.transaction('sessions', 'readonly');
        const store = transaction.objectStore('sessions');
        const request = store.getAll();

        request.onsuccess = (event) => {
          const sessions = event.target.result;

          if (sessions.length === 0) {
            console.log('No sessions found in the database.');
            resolve(null); // No active session
            return;
          }

          // Filter for the current session (if multiple, return the first active one)
          const currentSession = sessions.find(session => session.is_active);

          if (currentSession) {
            console.log('Current session found:', currentSession);
            resolve(currentSession);
          } else {
            console.log('No active session found.');
            resolve(null);
          }
        };

        request.onerror = (event) => {
          console.error('Error fetching sessions:', event.target.error);
          reject(event.target.error);
        };
      })
      .catch((error) => {
        console.error('Error opening database:', error);
        reject(error);
      });
  });
}


function generateSession(userType) {
  console.log(`calling generate_${userType}_auth_unique_id`);

  // Fetch the current session (if any)
  getCurrentSession()
    .then((currentSession) => {
      if (currentSession) {
        // If a current session exists, delete it
        deleteSession(currentSession.id);
        console.log(`Deleted existing session: ${currentSession.id}`);
      }

      // Create the new session
      const sessionObj = {
        is_active: false, // Set the new session as active
        id: generateUniqueId(),
        created_at: Date.now().toString(),
        updated_at: Date.now().toString(),
        ttl: 1 * 60 * 60 * 1000, // TTL set to 1 hours in milliseconds
        user_type: userType,
      };

      // Persist the new session
      persist(sessionObj.id, sessionObj);

      console.log(`New session created and persisted for userType: ${userType}`);
      console.log(sessionObj); // Log the session object for confirmation
      return sessionObj; // Return the session object if needed
    })
    .catch((error) => {
      console.error('Error while handling session generation:', error);
    });
}


function addSessionTTL(userType) {
  console.log('calling add_session_ttl');
  let ttlHours;

  switch (userType) {
      case 'first':
          ttlHours = 1; // 1 hour
          break;
      case 'customer':
          ttlHours = 48; // 48 hours
          break;
      case 'vendor':
          ttlHours = 72; // 72 hours
          break;
      default:
          console.error('Invalid user type');
          return 0;
  }

  return ttlHours * 60 * 60 * 1000; // Convert hours to milliseconds
}

function determineUserSessionTTL() {
  return getCurrentSession()
    .then((currentSession) => {
      if (!currentSession) {
        console.log('No active session found.');
        return -1; // No valid session found
      }

      const currentTime = Date.now();
      const sessionExpiry = parseInt(currentSession.created_at) + parseInt(currentSession.ttl);

      if (currentTime >= sessionExpiry) {
        console.log('Session has expired:', currentSession.id);
        deleteSession(currentSession.id);
        return -1; // Session expired
      } else {
        const remainingTtl = sessionExpiry - currentTime;
        console.log(`Remaining TTL for session ${currentSession.id}: ${remainingTtl} ms`);
        return remainingTtl; // Return the remaining TTL
      }
    })
    .catch((error) => {
      console.error('Error determining session TTL:', error);
      return -1; // Return -1 in case of an error
    });
}


function handleFirstTimeContact() {
  console.log('Handling first-time contact');

  return getCurrentSession()
    .then((currentSession) => {
      if (currentSession) {
        const ttlStatus = determineUserSessionTTL();
        console.log(`fetched ttlStatus is ${ttlStatus}`)

        return ttlStatus.then((remainingTTL) => {
          if (remainingTTL > 0) {
            console.log('Active session found:', currentSession);
            return currentSession; // Return the current active session
          } else {
            console.log('Session expired. Clearing session:', currentSession.id);
            deleteSession(currentSession.id);
            return createNewFirstSession(); // Generate a new session if expired
          }
        });
      } else {
        console.log('No active session found. Generating new first session.');
        return createNewFirstSession(); // Generate a new session if none exists
      }
    })
    .catch((error) => {
      console.error('Error handling first-time contact:', error);
    });
}

function createNewFirstSession() {
  const newSession = JSON.parse(generateSession('first'));
  newSession.ttl = addSessionTTL(newSession.user_type);
  persist(newSession.id, newSession);

  console.log('New session created:', newSession);
  return newSession;
}


function generateUniqueId() {
  return [...Array(32)].map(() => Math.floor(Math.random() * 16).toString(16)).join('');
}

function is_active() {
  return getCurrentSession()
    .then((session) => {
      if (session && session.is_active) {
        console.log(`Current session is active.`);
        return true;
      } else {
        console.log(`Current session is not active.`);
        return false;
      }
    })
    .catch((error) => {
      console.error('Error checking active status for the current session:', error);
      return false;
    });
}

function set_inactive() {
  return getCurrentSession()
    .then((session) => {
      if (session) {
        session.is_active = false;
        session.updated_at = Date.now().toString();
        persist(session.id, session); // Persist the updated session
        console.log(`Current session set to inactive.`);
      } else {
        console.log(`No current session found to set inactive.`);
      }
    })
    .catch((error) => {
      console.error('Error setting the current session to inactive:', error);
    });
}


function is_first() {
  return getCurrentSession()
    .then((session) => {
      if (session && session.user_type === 'first') {
        console.log(`Current session is a first-time session.`);
        return true;
      } else {
        console.log(`Current session is not a first-time session.`);
        return false;
      }
    })
    .catch((error) => {
      console.error('Error checking first-time session status:', error);
      return false;
    });
}

function is_customer() {
  return getCurrentSession()
    .then((session) => {
      if (session && session.user_type === 'customer') {
        console.log(`Current session is a customer session.`);
        return true;
      } else {
        console.log(`Current session is not a customer session.`);
        return false;
      }
    })
    .catch((error) => {
      console.error('Error checking customer session status:', error);
      return false;
    });
}

function is_vendor() {
  return getCurrentSession()
    .then((session) => {
      if (session && session.user_type === 'vendor') {
        console.log(`Current session is a vendor session.`);
        return true;
      } else {
        console.log(`Current session is not a vendor session.`);
        return false;
      }
    })
    .catch((error) => {
      console.error('Error checking vendor session status:', error);
      return false;
    });
}


function process_render() {
  console.log('calling process_render');

  
  sess_ttl = determineUserSessionTTL();

  // if (sess_ttl > 0) {
  //   console.log(`session still count at : ${sess_ttl}`);
  //   set_active_status(true);
  // } else {
  //   console.log(`session has expired at ${sess_ttl}`);
  //   set_active_status(false);
  // }

  const userType = is_first() ? 'first' 
                 : is_customer() ? 'customer' 
                 : is_vendor() ? 'vendor' 
                 : 'unknown';

  switch (userType) {
    case 'first':
      console.log('is first user');
      if (sess_ttl > 0) {
        show_first_active();
      } else {
        show_first_inactive();
      }
      break;

    case 'customer':
      console.log('is customer user');
      if (sess_ttl > 0) {
        show_customer_active();
      } else {
        show_customer_inactive();
      }
      break;

    case 'vendor':
      console.log('is vendor user');
      if (sess_ttl > 0) {
        show_vendor_active();
      } else {
        show_vendor_inactive();
      }
      break;

    default:
      console.log('Unknown user type');
  }
}

// checking storage mechanisms available: comparing normal vs miniBrowser environment
function checkAndDisplayStorageMechanisms() {
  let message = "Storage Mechanisms Report:\n\n";

  // Check localStorage
  try {
      if (window.localStorage) {
          const localStorageKeys = Object.keys(localStorage);
          message += `localStorage: Available\n`;
          if (localStorageKeys.length > 0) {
              message += "Contents:\n";
              localStorageKeys.forEach(key => {
                  message += `  ${key}: ${localStorage.getItem(key)}\n`;
              });
          } else {
              message += "  No data found.\n";
          }
      } else {
          message += "localStorage: Not Supported\n";
      }
  } catch (error) {
      message += `localStorage: Error (${error.message})\n`;
  }

  // Check sessionStorage
  try {
      if (window.sessionStorage) {
          const sessionStorageKeys = Object.keys(sessionStorage);
          message += `\nsessionStorage: Available\n`;
          if (sessionStorageKeys.length > 0) {
              message += "Contents:\n";
              sessionStorageKeys.forEach(key => {
                  message += `  ${key}: ${sessionStorage.getItem(key)}\n`;
              });
          } else {
              message += "  No data found.\n";
          }
      } else {
          message += "sessionStorage: Not Supported\n";
      }
  } catch (error) {
      message += `sessionStorage: Error (${error.message})\n`;
  }

  // Check IndexedDB
  try {
      if (window.indexedDB) {
          message += `\nIndexedDB: Available\n`;

          const request = indexedDB.open("testDB");

          request.onsuccess = function (event) {
              const db = event.target.result;
              const transaction = db.transaction(db.objectStoreNames, "readonly");

              const dbContents = [];
              let processedStores = 0;

              Array.from(db.objectStoreNames).forEach(storeName => {
                  const store = transaction.objectStore(storeName);
                  const getAllRequest = store.getAll();

                  getAllRequest.onsuccess = function () {
                      dbContents.push(`Contents of ${storeName}:\n`);
                      getAllRequest.result.forEach((item, index) => {
                          dbContents.push(`  ${index + 1}: ${JSON.stringify(item)}\n`);
                      });

                      processedStores++;
                      if (processedStores === db.objectStoreNames.length) {
                          message += dbContents.join("") || "  No data found.\n";
                          // Final alert after IndexedDB data
                          alert(message);
                      }
                  };

                  getAllRequest.onerror = function () {
                      dbContents.push(`  Unable to retrieve data for ${storeName}.\n`);
                      processedStores++;
                      if (processedStores === db.objectStoreNames.length) {
                          message += dbContents.join("") || "  No data found.\n";
                          alert(message);
                      }
                  };
              });
          };

          request.onerror = function () {
              message += "Unable to open IndexedDB or retrieve data.\n";
              alert(message);
          };
      } else {
          message += "IndexedDB: Not Supported\n";
      }
  } catch (error) {
      message += `IndexedDB: Error (${error.message})\n`;
  }

  // Check cookies
  try {
      if (navigator.cookieEnabled) {
          const cookies = document.cookie.split("; ");
          message += `\nCookies: Enabled\n`;
          if (cookies.length > 0 && cookies[0] !== "") {
              message += "Contents:\n";
              cookies.forEach(cookie => {
                  message += `  ${cookie}\n`;
              });
          } else {
              message += "  No cookies found.\n";
          }
      } else {
          message += "Cookies: Disabled\n";
      }
  } catch (error) {
      message += `Cookies: Error (${error.message})\n`;
  }

  // Display alert for non-IndexedDB mechanisms
  alert(message);
}


// add-on fix later
var is_pr_activated = true;

function activate_pr_browse() {
  console.log('calling activate_pr_browse');
  is_pr_activated = true; // Activate PR browsing
  console.log('PR browsing activated.');
}

function deactivate_pr_browse() {
  console.log('calling deactivate_pr_browse');
  is_pr_activated = false; // Deactivate PR browsing
  console.log('PR browsing deactivated.');
}

function check_pr_activated() {
  console.log('calling check_pr_activated');
  if (is_pr_activated) {
    console.log('PR browsing is activated.');
    return true;
  } else {
    console.log('PR browsing is not activated.');
    return false;
  }
}





