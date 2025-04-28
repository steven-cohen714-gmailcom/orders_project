import { loadRequesters, loadSuppliers } from './components/shared_filters.js';       
import { expandLineItems } from './components/expand_line_items.js';       
import { showUploadAttachmentsModal, checkAttachments, showViewAttachmentsModal } from './components/attachment_modal.js';       
import { showOrderNoteModal, showSupplierNoteModal } from './components/order_note_modal.js';       
import { showReceiveModal } from './components/receive_modal.js';

async function loadFiltersAndOrders() {       
 try {    
     await Promise.all([       
         loadRequesters("filter-requester").catch(err => { console.error("Failed to load requesters:", err); throw err; }),       
         loadSuppliers("filter-supplier").catch(err => { console.error("Failed to load suppliers:", err); throw err; })       
     ]);       
     console.log("Filters loaded successfully");   
     await loadOrders();       
 } catch (error) {    
     console.error("Error loading filters or orders:", error);    
     document.getElementById("pending-body").innerHTML = '<tr><td colspan="7">Error loading filters: ' + escapeHTML(error.message) + '</td></tr>';    
 }    
}

function escapeHTML(str) {      
 if (typeof str !== 'string') return '';      
 return str      
     .replace(/&/g, '&amp;')      
     .replace(/</g, '&lt;')      
     .replace(/>/g, '&gt;')      
     .replace(/"/g, '&quot;')      
     .replace(/'/g, '&#39;');  
}

async function loadOrders() {       
 const startDate = document.getElementById("start-date").value;       
 const endDate = document.getElementById("end-date").value;       
 const requester = document.getElementById("filter-requester").value;       
 const supplier = document.getElementById("filter-supplier").value;       
 const status = document.getElementById("filter-status").value;

 const params = new URLSearchParams();       
 if (startDate) params.append("start_date", startDate);       
 if (endDate) params.append("end_date", endDate);       
 if (requester && requester !== "All") params.append("requester", requester);       
 if (supplier && supplier !== "All") params.append("supplier", supplier);       
 if (status && status !== "All") params.append("status", status);

 try {       
     console.log("Fetching orders with params:", params.toString());   
     const res = await fetch(`/orders/api/orders/pending_orders?${params.toString()}`);       
     if (!res.ok) {       
         const errorText = await res.text();       
         throw new Error(`HTTP error! Status: ${res.status}, Message: ${errorText}`);       
     }       
     const data = await res.json();

     console.log("Pending Orders API Response:", JSON.stringify(data, null, 2));

     const tbody = document.getElementById("pending-body");       
     tbody.innerHTML = "";

     if (data.orders && Array.isArray(data.orders) && data.orders.length > 0) {       
         data.orders.forEach((order, index) => {       
             const row = document.createElement("tr");       
             const sanitizedOrderNote = escapeHTML(order.order_note || "");       
             const sanitizedSupplierNote = escapeHTML(order.note_to_supplier || "");       
             const sanitizedOrderNumber = escapeHTML(order.order_number || "");       
             const sanitizedSupplier = escapeHTML(order.supplier || "N/A");       
             const sanitizedRequester = escapeHTML(order.requester || "N/A");       
             const sanitizedDate = escapeHTML(order.created_date || "");       
             const sanitizedTotal = order.total != null ? `R${parseFloat(order.total).toFixed(2)}` : "R0.00";       
             const sanitizedStatus = escapeHTML(order.status || "");       
             row.innerHTML = `       
                 <td>${sanitizedDate}</td>       
                 <td>${sanitizedOrderNumber}</td>       
                 <td>${sanitizedRequester}</td>       
                 <td>${sanitizedSupplier}</td>       
                 <td>${sanitizedTotal}</td>       
                 <td><span class="status">${sanitizedStatus}</span></td>       
                 <td>       
                     <span class="expand-icon" data-order-id="${order.id || ''}">⬇️</span>       
                     <span class="clip-icon" title="View/Upload Attachments" data-order-id="${order.id || ''}" data-order-number="${sanitizedOrderNumber}">📎</span>       
                     <span class="note-icon" title="Edit Order Note" data-order-id="${order.id || ''}" data-order-note="${sanitizedOrderNote}" id="order-note-${index}">📝</span>       
                     <span class="supplier-note-icon" title="View Note to Supplier" data-supplier-note="${sanitizedSupplierNote}" data-order-number="${sanitizedOrderNumber}" id="supplier-note-${index}">📦</span>       
                     <span class="receive-icon" title="Mark as Received" data-order-id="${order.id || ''}" data-order-number="${sanitizedOrderNumber}">✅</span>       
                 </td>       
             `;       
             tbody.appendChild(row);

             // Attach event listeners programmatically       
             row.querySelector(`#supplier-note-${index}`).addEventListener("click", () => {       
                 try {       
                     window.showSupplierNoteModal(sanitizedSupplierNote);       
                 } catch (e) {       
                     console.error(`Failed to show supplier note for order ${sanitizedOrderNumber}:`, e);       
                     alert(`Error displaying supplier note: ${e.message}`);       
                 }       
             });       
             row.querySelector(`#order-note-${index}`).addEventListener("click", (e) => {       
                 const target = e.target;       
                 window.showOrderNoteModal(sanitizedOrderNote, order.id || '', (newNote) => {       
                     // Update the data-order-note attribute in the DOM       
                     target.setAttribute("data-order-note", escapeHTML(newNote));       
                 });       
             });       
             row.querySelector(".expand-icon").addEventListener("click", (e) => window.expandLineItems(order.id || '', e.target));       
             row.querySelector(".clip-icon").addEventListener("click", (e) => {       
                 const target = e.target;       
                 window.checkAttachments(order.id || '').then(has => {       
                     if (has) {       
                         window.showViewAttachmentsModal(order.id || '', sanitizedOrderNumber);       
                     } else {       
                         window.showUploadAttachmentsModal(order.id || '', sanitizedOrderNumber, () => {       
                             window.checkAttachments(order.id || '').then(has => target.classList.toggle('eye-icon', has));       
                         });       
                     }       
                 });       
             });       
             row.querySelector(".receive-icon").addEventListener("click", () => window.showReceiveModal(order.id || '', sanitizedOrderNumber));       
         });       
     } else {       
         tbody.innerHTML = '<tr><td colspan="7">No pending orders found.</td></tr>';       
     }       
 } catch (error) {       
     console.error("Error loading orders:", error);       
     document.getElementById("pending-body").innerHTML = '<tr><td colspan="7">Error loading orders: ' + escapeHTML(error.message) + '</td></tr>';       
 }       
}

function clearFilters() {       
 document.getElementById("start-date").value = "";       
 document.getElementById("end-date").value = "";       
 document.getElementById("filter-requester").value = "All";       
 document.getElementById("filter-supplier").value = "All";       
 document.getElementById("filter-status").value = "All";       
 loadOrders();       
}

// Event listeners       
document.getElementById("run-btn").addEventListener("click", loadOrders);       
document.getElementById("clear-btn").addEventListener("click", clearFilters);

// Initial load       
document.addEventListener("DOMContentLoaded", loadFiltersAndOrders);

// Expose functions to global scope for onclick handlers (if needed elsewhere)       
window.expandLineItems = expandLineItems;       
window.showUploadAttachmentsModal = showUploadAttachmentsModal;       
window.checkAttachments = checkAttachments;       
window.showViewAttachmentsModal = showViewAttachmentsModal;       
window.showOrderNoteModal = showOrderNoteModal;       
window.showSupplierNoteModal = showSupplierNoteModal;       
window.showReceiveModal = showReceiveModal;