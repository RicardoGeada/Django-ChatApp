  /**
   * 
   */
  async function sendMessage() {
    let fd = createFormData();
    let pendingMessageId = addChatMessage({created_at : formatDateForMessage(), author: username.value, text: messageField.value, state: 'pending'});
    let json;
    try {
      let response = await fetch("/chat/", { method: "POST", body: fd,});
      json = await response.json(); // string in json umwandeln
      if(typeof json != Object) json = JSON.parse(json);
    } 
    catch (e) {
      console.error(e);
    } 
    finally { 
      handleJsonResponse(json, pendingMessageId);
    }
  }


  /**
   * creates FormData
   * @returns FormData
   */
  function createFormData() {
    let fd = new FormData();
    let token = document.querySelector('[name=csrfmiddlewaretoken]').value;
    fd.append("textmessage", messageField.value);
    fd.append("csrfmiddlewaretoken", token);
    return fd;
  }

  
  /**
   * Handle the post request response
   * @param {JSON} json - json response from POST request
   * @param {Number} pendingMessageId - Id from the pending message
   */
  function handleJsonResponse(json, pendingMessageId) {
    if (json) {
      document.getElementById(pendingMessageId).remove();
      addChatMessage({created_at: formatDateForMessage(json.fields.created_at), author: username.value, text: json.fields.text});
    }
    else {
      document.getElementById(pendingMessageId).classList.remove('pending');
      document.getElementById(pendingMessageId).classList.add('error');
    }
    messageField.value = '';
  }


  /**
   * add a new message to the chat
   * @param created_at - The time the message was created.
   * @param author - The author of the message.
   * @param text - The text of the message. 
   * @param state - CSS Classes for the state of the message. pending / error
   * @returns id
   */
  function addChatMessage({created_at,author,text,state}) {
    let id = setMessageId();
    messageContainer.innerHTML += `
    <div id="${ id }" class="chat-message ${state}">
      <span class="time">[${ formatDateForMessage(created_at) }]</span>
      ${ author }:
      <i class="text">${ text }</i>
    </div>
   `;
   return id;
  }


  /**
   * generates a new ID that is incremented by one from the highest existing ID
   * @returns new id
   */
  function setMessageId() {
    const messages = document.getElementsByClassName('chat-message');
    const ids = Array.from(messages, (message) => parseInt(message.id));
    const highestId = Math.max(...ids);
    return highestId + 1;
  }


  /**
   * creates / formats date for message
   * @param {*} dateInput - eligible parameter for new Date()
   * @returns date in format [Month Day, Year]
   */
  function formatDateForMessage(dateInput) {
    const date = dateInput ?  new Date(dateInput) : new Date();
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    const formattedDate = date.toLocaleDateString('en-US', options);
    return `${formattedDate}`;
  }
  