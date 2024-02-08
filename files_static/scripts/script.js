// Função enviar dados para a views delete_or_archive
document.addEventListener("DOMContentLoaded", function () {
  var conversationsTab = document.getElementById("conversations-tab");
  var onlineUsersTab = document.getElementById("online-users-tab");
  var archiveUsersTab = document.getElementById("archive-users-tab");

  onlineUsersTab.style.position = "relative";
  archiveUsersTab.style.position = "relative";

  var conversationsList = document.querySelector(".user-list.conversations");
  var onlineList = document.querySelector(".user-list.online");
  var archiveList = document.querySelector(".user-list.archive"); // Corrigido o seletor

  // Adiciona um listener de clique à aba "Conversas"
  conversationsTab.addEventListener("click", function () {
    conversationsList.classList.remove("hidden");
    onlineList.classList.add("hidden");
    archiveList.classList.add("hidden"); // Oculta a lista de arquivo ao clicar em "Conversas"

    conversationsTab.style.borderBottom = "2px solid white";
    onlineUsersTab.style.borderBottom = "none";
    archiveUsersTab.style.borderBottom = "none";
  });

  // Adiciona um listener de clique à aba "Online"
  onlineUsersTab.addEventListener("click", function () {
    conversationsList.classList.add("hidden");
    onlineList.classList.remove("hidden");
    archiveList.classList.add("hidden");

    onlineUsersTab.style.borderBottom = "2px solid white";
    conversationsTab.style.borderBottom = "none";
    archiveUsersTab.style.borderBottom = "none";
  });

  // Adiciona um listener de clique à aba "Arquivo"
  archiveUsersTab.addEventListener("click", function () {
    conversationsList.classList.add("hidden");
    onlineList.classList.add("hidden");
    archiveList.classList.remove("hidden"); // Exibe a lista de arquivo ao clicar em "Arquivo"

    conversationsTab.style.borderBottom = "none";
    onlineUsersTab.style.borderBottom = "none";
    archiveUsersTab.style.borderBottom = "2px solid white";
  });
});

// Get the submenu
function toggleSubmenu() {
  var submenu = document.getElementById("submenu");
  submenu.classList.toggle("visible");
}

// Get the modal
var modal = document.getElementById("id01");

// When the user clicks anywhere outside of the modal, close it
window.onclick = function (event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
};

const usersDataString = document.getElementById("data").innerText;
const usersData = JSON.parse(usersDataString.replace('">', ""));

function searchUsers() {
  const searchInput = document.getElementById("searchInput");
  const searchTerm = searchInput.value.toLowerCase();
  const searchResults = document.getElementById("searchResults");

  // Limpa os resultados anteriores
  searchResults.innerHTML = "";

  if (searchTerm === "") {
    // Se o campo de pesquisa estiver vazio, não há resultados
    return;
  }

  const filteredUsers = usersData.filter((userData) =>
    userData.name.toLowerCase().includes(searchTerm)
  );

  if (filteredUsers.length === 0) {
    // Se nenhum usuário for encontrado, exibe a mensagem
    const noResultsMessage = document.createElement("div");
    noResultsMessage.textContent = "Nenhum usuário encontrado";
    searchResults.appendChild(noResultsMessage);
    return;
  }

  filteredUsers.forEach((user) => {
    const resultItem = document.createElement("div");
    resultItem.classList.add("search-result");

    // Adiciona o contêiner para a foto do usuário
    const userPhotoContainer = document.createElement("div");
    userPhotoContainer.classList.add("user-photo-container");

    // Adiciona a imagem do usuário
    const userPhoto = document.createElement("img");
    userPhoto.src = user.photo;
    userPhoto.alt = user.name;
    userPhoto.classList.add("user-photo");

    // Adiciona o nome do usuário
    const userName = document.createElement("span");
    userName.textContent = user.name;

    // Adiciona a imagem e o nome ao contêiner
    userPhotoContainer.appendChild(userPhoto);
    userPhotoContainer.appendChild(userName);

    resultItem.appendChild(userPhotoContainer);

    resultItem.addEventListener("click", () =>
      selectUser(user.name, user.token)
    );

    searchResults.appendChild(resultItem);
  });
}

function selectUser(user, token) {
  const selectedUsersDisplay = document.getElementById("selectedUsersDisplay");
  selectedUsersDisplay.innerHTML = `Para: <b>${user}</b>`;

  const submitButton = document.getElementById("submitButton");

  if (submitButton) {
    submitButton.addEventListener("click", function (event) {
      event.preventDefault(); // Evita o comportamento padrão do formulário
      host = window.location.host;
      window.location.href = `http://${host}/chat/${token}/`;
    });
  }
}

function activateInput(inputId) {
  const input = document.getElementById(inputId);

  // Torna visível o input associado ao botão clicado
  input.style.display = "block";

  // Clique no input para abrir a caixa de diálogo diretamente
  input.click();

  input.style.display = "none";
}

function selectMedia(type, input) {
  const selectedMediaContainer = document.getElementById("selectedMedia");
  var submenuButton = document.getElementById("submenu-icon");

  // Remove a mídia anterior, se houver
  selectedMediaContainer.innerHTML = "";

  // Adiciona o ícone e o nome da mídia selecionada
  const mediaIcon = document.createElement("div");
  const mediaIcons = {
    image: '<i class="fas fa-image"></i> Imagem',
    video: '<i class="fas fa-file-video"></i> Vídeo',
    pdf: '<i class="fas fa-file-pdf"></i> PDF',
  };
  mediaIcon.innerHTML = mediaIcons[type];
  selectedMediaContainer.appendChild(mediaIcon);

  // Adiciona o nome do arquivo
  const fileName = document.createElement("div");
  if (input.files.length > 0 && input.files[0].name) {
    fileName.textContent = `Arquivo selecionado: ${input.files[0].name}`;
  } else {
    fileName.innerHTML = `Arquivo selecionado: <b style="color: red;">Nenhum arquivo selecionado</b>`;
  }
  selectedMediaContainer.appendChild(fileName);

  // Adiciona o botão de remoção
  const removeButton = document.createElement("button");
  removeButton.innerHTML = "&times;"; // Símbolo "x"
  removeButton.addEventListener("click", function () {
    // Remove a mídia selecionada
    selectedMediaContainer.innerHTML = "";
    // Limpa o input file
    input.value = "";
  });
  selectedMediaContainer.appendChild(removeButton);

  submenuButton.click(); // Feche o submenu após enviar a mídia

  // Crie o WebSocket fora da função
  const chatSocket = new WebSocket(
    "ws://" + window.location.host + "/ws/chat/" + roomName + "/"
  );

  chatSocket.onopen = function () {
    console.log("WebSocket aberto com sucesso");
  };

  chatSocket.onclose = function (e) {
    console.error("Chat socket closed unexpectedly");
  };

  // Aqui você pode processar o arquivo, se necessário
  function minhaFuncao() {
    const selectedFile = input.files[0];

    // Leia o conteúdo do arquivo como base64
    const reader = new FileReader();

    reader.onload = function (e) {
      // Extraia o tipo de mídia do arquivo, se necessário
      const type = selectedFile.type;

      // Envie a mídia com o conteúdo do arquivo em base64
      const data = {
        type: type,
        mediaPath: reader.result, // Altere para reader.result
      };

      chatSocket.send(JSON.stringify(data));
    };

    reader.readAsDataURL(selectedFile);
    document
      .querySelector("#chat-message-submit")
      .removeEventListener("click", minhaFuncao);
  }

  // Evento quando a tecla Enter é pressionada no input
  document.querySelector("#message-input").focus();
  document.querySelector("#message-input").onkeyup = function (e) {
    if (e.key === "Enter") {
      // enter, return
      document.querySelector("#chat-message-submit").click();
    }
  };

  // Evento quando o botão é clicado
  document
    .querySelector("#chat-message-submit")
    .addEventListener("click", minhaFuncao);
}

// Função para enviar dados para a views delete_or_archive e para abrir e fechar o submenu do user.
const contextMenus = document.querySelectorAll(".dot");

contextMenus.forEach(function (contextMenu) {
  contextMenu.addEventListener("click", function (event) {
    const dot = event.target.closest(".dot");

    if (dot) {
      const submenu = dot.querySelector(".submenu-conversation");

      // Oculta todos os submenus
      document
        .querySelectorAll(".submenu-conversation")
        .forEach(function (otherSubmenu) {
          if (otherSubmenu !== submenu) {
            otherSubmenu.style.display = "none";
          }
        });

      if (submenu.style.display === "none" || !submenu.style.display) {
        submenu.style.display = "block";

        // Adiciona um listener de clique para o submenu
        submenu.addEventListener("click", function (event) {
          const button = event.target.closest("button");
          const input = submenu.querySelector("input");

          // Verifica se o alvo do clique é um botão
          if (button) {
            // Obtém o valor do botão clicado
            const buttonValue = button.value;

            // Atribui o valor ao input com ID "buttonClicked"
            input.value = buttonValue;
          }
        });
      } else {
        submenu.style.display = "none";
      }
    }
  });
});

// ###################################################

var chatMessagesDiv = document.querySelector(".chat-messages");
chatMessagesDiv.scrollTop = chatMessagesDiv.scrollHeight;

// ###################################################

var modal = document.getElementById("myFile");

// Get the image and insert it inside the modal - use its "alt" text as a caption
var img = document.querySelector("#myImg");
var modalImg = document.getElementById("imgfile");
img.onclick = function () {
  modal.style.display = "block";
  modalImg.src = this.src;
};

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// When the user clicks on <span> (x), close the modal
span.onclick = function () {
  modal.style.display = "none";
};

// ###################################################
// Função para enviar mensagem no websocket]

// Função AJAX para recarregar em segundo plano
function reloadIn(callback) {
  host = window.location.host;

  var xhr = new XMLHttpRequest();

  // Configurar a requisição
  xhr.open("GET", `http://${host}/chat/${currentUser}/`, true);

  // Definir o callback quando a requisição for concluída
  xhr.onload = function () {
    if (xhr.status >= 200 && xhr.status < 300) {
      // A resposta foi bem-sucedida, você pode fazer algo com a resposta se necessário

      console.log("Resposta recebida");
      var parser = new DOMParser();
      var ajaxResponse = parser.parseFromString(xhr.responseText, "text/html");

      // Verificar se o callback é uma função antes de chamá-lo
      if (typeof callback === "function") {
        // Chamar o callback (addConversation) e passar a resposta como argumento

        callback(ajaxResponse);
      }
    } else {
      // A requisição falhou
      console.error("Erro ao recarregar em segundo plano");
    }
  };

  // Enviar a requisição
  xhr.send();
}

function reloadInBackground(callback, id_chat) {
  host = window.location.host;

  var xhr = new XMLHttpRequest();

  // Configurar a requisição
  xhr.open("GET", `http://${host}/chat/${id_chat}/`, true);

  // Definir o callback quando a requisição for concluída
  xhr.onload = function () {
    if (xhr.status >= 200 && xhr.status < 300) {
      // A resposta foi bem-sucedida, você pode fazer algo com a resposta se necessário

      console.log("Resposta recebida");
      var parser = new DOMParser();
      var ajaxResponse = parser.parseFromString(xhr.responseText, "text/html");

      // Verificar se o callback é uma função antes de chamá-lo
      if (typeof callback === "function") {
        // Chamar o callback (addConversation) e passar a resposta como argumento
        callback(ajaxResponse);
      }
    } else {
      // A requisição falhou
      console.error("Erro ao recarregar em segundo plano");
    }
  };

  // Enviar a requisição
  xhr.send();
}

// Função para criar e adicionar elementos à div de mensagem
function addConversation(data) {
  reloadInBackground(function (ajaxResponse) {
    // Manipular a resposta do AJAX conforme necessário
    const existingContainer = ajaxResponse.querySelector(
      ".user-list.conversations"
    );

    // Substituir o conteúdo existente pelo novo conteúdo
    const userLists = document.querySelector(".user-list.conversations");
    userLists.innerHTML = existingContainer.innerHTML;

    // Verifica se a lista foi encontrada
    if (userLists) {
      // Obtém todas as tags li dentro da lista
      const listItems = userLists.querySelectorAll("li");

      // Itera sobre cada li
      let tokenExists = false;
      listItems.forEach((li) => {
        // Obtém todos os spans dentro da li
        const spans = li.querySelectorAll("span");

        let tagLiUser = "";

        // Verifica se o token já existe em alguma li
        tokenExists = Array.from(listItems).some((li) => {
          const span = li.querySelector("span");
          if (span.textContent === data.sender_token) {
            tagLiUser = li;
          }
          return span && span.textContent === data.sender_token;
        });

        if (tokenExists) {
          const tagP = tagLiUser.querySelector(`#tagContent`);

          // Cria um novo elemento span
          const newSmall = tagLiUser.querySelector(".badge");
          newSmall.textContent = data.count_notification;

          // Atualiza o conteúdo e o estilo do span original
          tagP.textContent = `${data.message}`;
          tagP.style.fontWeight = "bolder";

          // Adiciona o li correspondente ao topo da lista
          // userLists.insertBefore(tagLiUser, userLists.firstChild);
        }
      });

      // if (!tokenExists && !data.existMessage) {
      //   // Se o token não existir em nenhuma li, crie uma nova li
      //   // ...

      //   const none = document.querySelector("#none");

      //   if (none) {
      //     none.style.display = "none";
      //   }

      //   const ul = document.createElement("ul");
      //   ul.classList.add("user-list", "conversations");

      //   const listItem = document.createElement("li");
      //   listItem.classList.add("user-list-item");

      //   listItem.innerHTML = `
      //     <img src="${data.receiver_img}" alt="${data.receiver}" />

      //     ${data.count_notify !== 0 ? `<small class="badge">${data.count_notification}</small>` : ''}

      //     <div class="user-list-item-info">
      //       <h3>${data.receiver_name}</h3>
      //       ${
      //         data.message
      //           ? `<p id="tagContent">${data.message}</p>`
      //           : `<p>Enviou uma mídia...</p>`
      //       }
      //       <span style="display: none;">${data.token}</span>
      //     </div>
      //   `;

      //   const formItem = document.createElement("form");
      //   formItem.action = `{% url 'delete_or_archive' ${data.token} %}`;
      //   formItem.method = "POST";

      //   formItem.innerHTML = `
      //     <div class="context-menu">
      //       <div class="dot">
      //         <img src="/static/img/opcoes.png" alt="opcoes-menu">
      //         <!-- Submenu -->
      //         <div class="submenu-conversation" style="display: none;">
      //           <input type="hidden" name="data" id="buttonClicked" value="">
      //           <span style="display: none;">${data.token}</span>
      //           <!-- Adicione aqui os itens do submenu com ícones -->
      //           <button type="submit" name="Delete" value="Delete">
      //             <i class="fas fa-trash"></i>
      //             Excluir
      //           </button>

      //           <button type="submit" name="Archive" value="Archive">
      //             <i class="fas fa-archive"></i>
      //             Arquivar
      //           </button>
      //         </div>
      //       </div>
      //     </div>
      //   `;

      //   const hr = document.createElement("hr");
      //   hr.classList.add("hr-line");

      //   ul.appendChild(listItem);
      //   ul.appendChild(formItem);
      //   ul.appendChild(hr);
      //   fatherDiv.appendChild(ul);
      // }
    } else {
      console.error(
        "Nenhum elemento .user-list.conversations encontrado na resposta do AJAX"
      );
    }
  }, data.receiver);
}

function addMessageToChat(chat, data, messageClass) {
  const messageDiv = document.createElement("div");
  messageDiv.classList.add("message", messageClass);

  const userImg = document.createElement("img");
  userImg.classList.add("user-img");
  userImg.src = data.sender_img;
  userImg.alt = data.sender;

  const messageInfoDiv = document.createElement("div");
  messageInfoDiv.classList.add("message-info");
  messageInfoDiv.innerHTML = `<span>${data.sender} • ${data.timestamp}</span>`;

  const messageTextDiv = document.createElement("div");
  messageTextDiv.classList.add("message-text");

  let content = "";

  if (data.img_file || data.pdf || data.video || data.message) {
    if (data.img_file) {
      content += `<img id="myImg" src="${data.img_file}" alt="" style="width:200px;max-width:200px;">
        <div id="myFile" class="file">
          <span class="close">&times;</span>
          <img class="modal-content" id="imgfile" alt="media-">
        </div>`;

      content += `
        <div class="read-recipient" title="Entregue há 2h">
          <i class="fas fa-check-double" style="color: black;"></i>
        </div>
      `;
    }

    if (data.pdf) {
      content += `<div class="pdf-container">
        <a class="pdf-button" href="${data.pdf}" target="_blank">
          <img class="pdf-image" src="{% static 'img/pdf.png' %}" alt="pdf-file" style="margin-left:-5px;">
          <div>
            <span class="pdf-name">nome do arquivo</span>
          </div>
        </a>
      </div>`;

      content += `
        <div class="read-recipient" title="Entregue há 2h">
          <i class="fas fa-check-double" style="color: black;"></i>
        </div>
      `;
    }

    if (data.video) {
      content += `<video width="100%" controls>
        <source src="${data.video}">
        Seu navegador não suporta o elemento de vídeo.
      </video>`;

      content += `
        <div class="read-recipient" title="Entregue há 2h">
          <i class="fas fa-check-double" style="color: black;"></i>
        </div>
      `;
    }

    if (data.message) {
      content += `<p>${data.message}</p>`;
      content += `
        <div class="read-recipient" title="Entregue há 2h">
          <i class="fas fa-check-double" style="color: black;"></i>
        </div>
      `;
    }

    messageTextDiv.innerHTML = content;
    messageDiv.appendChild(userImg);
    messageDiv.appendChild(messageInfoDiv);
    messageDiv.appendChild(messageTextDiv);
    chat.appendChild(messageDiv);
    chat.scrollTop = chat.scrollHeight;
  }
}

// #######################################################################
