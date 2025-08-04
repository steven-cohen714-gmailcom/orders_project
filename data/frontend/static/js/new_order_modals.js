export { showOrderNoteModal, showSupplierNoteModal } from './components/order_note_modal.js';

export function showViewAttachmentsModal(orderId, orderNumber, onUploadComplete = null, customFiles = null) {  
   // Use customFiles if provided, otherwise fetch attachments  
   const filesPromise = customFiles ? Promise.resolve({ attachments: customFiles }) : fetch(`/orders/attachments/${orderId}`).then(res => res.json());

   filesPromise  
       .then(data => {  
           const files = data.attachments || [];  
           const modal = createBaseModal();  
           const title = document.createElement("h3");  
           title.textContent = `Attachments for ${orderNumber}`;  
           modal.inner.appendChild(title);

           if (files.length > 0) {  
               const list = document.createElement("ul");  
               list.style.listStyle = "none";  
               list.style.padding = "0";

               files.forEach(f => {  
                   const li = document.createElement("li");  
                   const link = document.createElement("a");  
                   link.href = f.file_path;  
                   link.textContent = f.filename;  
                   link.target = "_blank";  
                   link.style.display = "block";  
                   link.style.marginBottom = "0.5rem";  
                   link.style.color = "green";  
                   link.style.textDecoration = "underline";  
                   li.appendChild(link);  
                   list.appendChild(li);  
               });

               modal.inner.appendChild(list);  
           }

           const dropzone = document.createElement("div");  
           dropzone.textContent = "Drag and drop files here or click to select";  
           dropzone.style.border = "2px dashed #aaa";  
           dropzone.style.padding = "2rem";  
           dropzone.style.textAlign = "center";  
           dropzone.style.cursor = "pointer";  
           dropzone.style.marginTop = "1rem";  
           dropzone.style.background = "#fafafa";

           dropzone.onclick = () => {  
               const input = document.createElement("input");  
               input.type = "file";  
               input.multiple = true;  
               input.onchange = () => handleFiles(input.files, orderId, modal.inner, onUploadComplete);  
               input.click();  
           };

           dropzone.ondragover = e => {  
               e.preventDefault();  
               dropzone.style.background = "#eee";  
           };  
           dropzone.ondragleave = () => {  
               dropzone.style.background = "#fafafa";  
           };  
           dropzone.ondrop = e => {  
               e.preventDefault();  
               dropzone.style.background = "#fafafa";  
               handleFiles(e.dataTransfer.files, orderId, modal.inner, onUploadComplete);  
           };

           modal.inner.appendChild(dropzone);

           const closeBtn = document.createElement("button");  
           closeBtn.textContent = "Close";  
           closeBtn.style.marginTop = "1.5rem";  
           closeBtn.style.padding = "0.5rem 1rem";  
           closeBtn.style.border = "none";  
           closeBtn.style.cursor = "pointer";  
           closeBtn.style.background = "#ccc";  
           closeBtn.onclick = () => document.body.removeChild(modal.container);

           modal.inner.appendChild(closeBtn);

           document.body.appendChild(modal.container);  
       })  
       .catch(err => {  
           alert("❌ Failed to load attachments");  
           console.error(err);  
       });  
}

export function handleFiles(fileList, orderId, modalInner, onUploadComplete = null) {  
   Array.from(fileList).forEach(file => {  
       const formData = new FormData();  
       formData.append("file", file);  
       formData.append("order_id", orderId);

       fetch("/orders/upload_attachment", {  
           method: "POST",  
           body: formData,  
       })  
           .then(res => res.json())  
           .then(data => {  
               const msg = document.createElement("p");  
               msg.textContent = data.status;  
               msg.style.color = "green";  
               modalInner.appendChild(msg);  
               if (onUploadComplete) onUploadComplete();  
           })  
           .catch(err => {  
               const msg = document.createElement("p");  
               msg.textContent = `❌ Failed to upload: ${file.name}`;  
               msg.style.color = "red";  
               modalInner.appendChild(msg);  
               console.error(err);  
           });  
   });  
}

export function createBaseModal() {  
   const container = document.createElement("div");  
   container.style.position = "fixed";  
   container.style.top = "0";  
   container.style.left = "0";  
   container.style.width = "100vw";  
   container.style.height = "100vh";  
   container.style.backgroundColor = "rgba(0,0,0,0.5)";  
   container.style.display = "flex";  
   container.style.alignItems = "center";  
   container.style.justifyContent = "center";  
   container.style.zIndex = "9999";

   const inner = document.createElement("div");  
   inner.style.backgroundColor = "white";  
   inner.style.padding = "1.5rem";  
   inner.style.borderRadius = "8px";  
   inner.style.width = "90%";  
   inner.style.maxWidth = "500px";  
   inner.style.maxHeight = "80vh";  
   inner.style.overflowY = "auto";  
   inner.style.fontFamily = "Arial, sans-serif";  
   inner.style.position = "relative";

   const close = document.createElement("button");  
   close.textContent = "✖";  
   close.style.position = "absolute";  
   close.style.top = "10px";  
   close.style.right = "10px";  
   close.style.background = "none";  
   close.style.border = "none";  
   close.style.fontSize = "1.2rem";  
   close.style.cursor = "pointer";  
   close.onclick = () => document.body.removeChild(container);

   inner.appendChild(close);  
   container.appendChild(inner);

   return { container, inner };  
}