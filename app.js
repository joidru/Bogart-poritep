// Product data is external to the UI logic. WordPress can replace this JSON endpoint.
let products=[];
const productsReady=fetch('products.json')
 .then(response=>{if(!response.ok)throw new Error('Не удалось загрузить товары');return response.json()})
 .then(data=>{products=Array.isArray(data)?data:[]})
 .catch(error=>{console.error(error);toast('Не удалось загрузить каталог товаров')});
const fmt=n=>new Intl.NumberFormat('ru-RU').format(n)+' ₽';
const getCart=()=>JSON.parse(localStorage.getItem('poritep-cart')||'{}');
const saveCart=c=>{localStorage.setItem('poritep-cart',JSON.stringify(c));updateCartCount()};
const cartCount=()=>Object.values(getCart()).reduce((a,b)=>a+b,0);
function toast(msg){const t=document.querySelector('#toast');if(!t)return;t.textContent=msg;t.classList.add('show');setTimeout(()=>t.classList.remove('show'),2500)}
function updateCartCount(){document.querySelectorAll('.cart-count').forEach(el=>el.textContent=cartCount())}
function addToCart(id,qty=1){const c=getCart();c[id]=(c[id]||0)+Number(qty);saveCart(c);toast('Товар добавлен в корзину')}
updateCartCount();
const menuButton=document.querySelector('.menu-button'),mobileNav=document.querySelector('.mobile-nav');
menuButton?.addEventListener('click',()=>{const open=mobileNav.classList.toggle('open');menuButton.setAttribute('aria-expanded',String(open));menuButton.setAttribute('aria-label',open?'Закрыть меню':'Открыть меню')});
document.addEventListener('keydown',e=>{if(e.key==='Escape'&&mobileNav?.classList.contains('open')){mobileNav.classList.remove('open');menuButton.setAttribute('aria-expanded','false');menuButton.setAttribute('aria-label','Открыть меню');menuButton.focus()}});
document.addEventListener('click',e=>{const b=e.target.closest('.add-cart');if(b)addToCart(b.dataset.id)});
const searchInput=document.querySelector('#searchInput'),searchResults=document.querySelector('#searchResults');
if(searchInput){
 searchInput.addEventListener('input',()=>{
  const query=searchInput.value.toLowerCase().trim();
  const found=query?products.filter(product=>product.name.toLowerCase().includes(query)).slice(0,5):[];
  searchResults.replaceChildren();
  found.forEach(product=>{
   const link=document.createElement('a');
   const image=document.createElement('img');
   const name=document.createElement('span');
   const price=document.createElement('b');
   link.className='search-result';
   link.href='product.html';
   image.src=product.image;
   image.alt='';
   name.textContent=product.name;
   price.textContent=fmt(product.price);
   link.append(image,name,price);
   searchResults.append(link);
  });
  searchResults.classList.toggle('open',found.length>0);
 });
 document.querySelector('.search').addEventListener('submit',event=>{
  event.preventDefault();
  location.href='catalog.html?q='+encodeURIComponent(searchInput.value);
 });
}
if(document.body.dataset.page==='product')initProductPage();
if(document.body.dataset.page==='cart')productsReady.then(renderCart);
if(searchInput)productsReady.then(()=>searchInput.dispatchEvent(new Event('input')));
function renderCart(){
 const cart=getCart();
 const wrap=document.querySelector('#cartContent');
 const items=Object.entries(cart).map(([id,qty])=>({product:products.find(item=>item.id===id),qty})).filter(item=>item.product);
 wrap.replaceChildren();

 if(!items.length){
  wrap.append(document.querySelector('#cartEmptyTemplate').content.cloneNode(true));
  return;
 }

 const layout=document.querySelector('#cartLayoutTemplate').content.cloneNode(true);
 const list=layout.querySelector('.cart-items');
 const itemTemplate=document.querySelector('#cartItemTemplate');
 items.forEach(({product,qty})=>{
  const item=itemTemplate.content.cloneNode(true);
  const image=item.querySelector('[data-cart-image]');
  image.src=product.image;
  image.alt=product.name;
  item.querySelector('[data-cart-name]').textContent=product.name;
  item.querySelector('[data-cart-meta]').textContent=`${product.size} · ${product.unit}`;
  item.querySelector('[data-cart-qty]').value=qty;
  item.querySelector('[data-cart-price]').textContent=fmt(product.price*qty);
  item.querySelectorAll('[data-change]').forEach(button=>{
   button.dataset.id=product.id;
   button.addEventListener('click',()=>{
    const next=getCart();
    next[product.id]=Math.max(1,next[product.id]+Number(button.dataset.change));
    saveCart(next);
    renderCart();
   });
  });
  const remove=item.querySelector('[data-remove]');
  remove.dataset.id=product.id;
  remove.addEventListener('click',()=>{
   const next=getCart();
   delete next[product.id];
   saveCart(next);
   renderCart();
  });
  list.append(item);
 });
 const total=items.reduce((sum,item)=>sum+item.product.price*item.qty,0);
 layout.querySelector('[data-cart-count]').textContent=cartCount();
 layout.querySelector('[data-cart-total]').textContent=fmt(total);
 wrap.append(layout);
}
document.querySelectorAll('form').forEach(f=>{f.noValidate=true;f.addEventListener('submit',e=>{f.classList.add('was-validated');if(!f.checkValidity()){e.preventDefault();e.stopImmediatePropagation();f.querySelector(':invalid')?.focus()}},true)});
document.querySelectorAll('.lead-form').forEach(f=>f.addEventListener('submit',e=>{e.preventDefault();f.reset();f.classList.remove('was-validated');toast('Заявка принята. Мы свяжемся с вами.')}));

const formatVolume=value=>new Intl.NumberFormat('ru-RU',{minimumFractionDigits:0,maximumFractionDigits:3}).format(value);

function initProductPage(){
 const product=document.querySelector('[data-product-detail]');
 if(!product)return;

 const infoTabs=[...document.querySelectorAll('[data-info-tab]')];
 const activateInfoTab=name=>{
  infoTabs.forEach(tab=>{
   const active=tab.dataset.infoTab===name;
   tab.classList.toggle('is-active',active);
   tab.setAttribute('aria-selected',String(active));
  });
  document.querySelectorAll('[data-info-panel]').forEach(panel=>{
   const active=panel.dataset.infoPanel===name;
   panel.hidden=!active;
   panel.classList.toggle('is-active',active);
  });
 };
 infoTabs.forEach((tab,index)=>{
  tab.addEventListener('click',()=>activateInfoTab(tab.dataset.infoTab));
  tab.addEventListener('keydown',event=>{
   if(!['ArrowLeft','ArrowRight'].includes(event.key))return;
   event.preventDefault();
   const direction=event.key==='ArrowRight'?1:-1;
   const next=infoTabs[(index+direction+infoTabs.length)%infoTabs.length];
   next.focus();
   activateInfoTab(next.dataset.infoTab);
  });
 });

 const volumeInput=document.querySelector('#calcVolume');
 const palletInput=document.querySelector('#calcPallets');
 if(!volumeInput||!palletInput)return;

 const productId=product.dataset.productId;
 const price=Number(product.dataset.price);
 const palletVolume=Number(product.dataset.palletVolume);
 const palletBlocks=Number(product.dataset.palletBlocks);
 let calculatedVolume=palletVolume;

 const drawCalculation=source=>{
  let pallets;
  if(source==='volume'){
   pallets=Math.max(1,Math.ceil((Number(volumeInput.value)||palletVolume)/palletVolume-1e-9));
  }else{
   pallets=Math.max(1,Math.round(Number(palletInput.value)||1));
   volumeInput.value=String(Math.round(pallets*palletVolume*1000)/1000);
  }
  palletInput.value=String(pallets);
  calculatedVolume=Math.round(pallets*palletVolume*1000)/1000;
  document.querySelector('#calcActualVolume').textContent=`${formatVolume(calculatedVolume)} м³`;
  document.querySelector('#calcResultBlocks').textContent=`${formatVolume(pallets*palletBlocks)} шт.`;
  const total=fmt(Math.round(calculatedVolume*price));
  document.querySelector('#calcTotal').textContent=total;
  document.querySelector('#calcButtonTotal').textContent=total;
 };
 volumeInput.addEventListener('input',()=>drawCalculation('volume'));
 palletInput.addEventListener('input',()=>drawCalculation('pallets'));
 document.querySelector('#calcVolumeMinus').addEventListener('click',()=>{
  volumeInput.value=String(Math.max(1,Math.round(((Number(volumeInput.value)||palletVolume)-1)*1000)/1000));
  drawCalculation('volume');
 });
 document.querySelector('#calcVolumePlus').addEventListener('click',()=>{
  volumeInput.value=String(Math.round(((Number(volumeInput.value)||palletVolume)+1)*1000)/1000);
  drawCalculation('volume');
 });
 document.querySelector('#calcPalletMinus').addEventListener('click',()=>{
  palletInput.value=Math.max(1,(Number(palletInput.value)||1)-1);
  drawCalculation('pallets');
 });
 document.querySelector('#calcPalletPlus').addEventListener('click',()=>{
  palletInput.value=(Number(palletInput.value)||1)+1;
  drawCalculation('pallets');
 });
 document.querySelector('#detailAdd').addEventListener('click',()=>addToCart(productId,calculatedVolume));
 drawCalculation('pallets');
}
