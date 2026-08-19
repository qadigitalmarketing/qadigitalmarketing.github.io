
document.addEventListener("DOMContentLoaded",()=>{
  const menu=document.querySelector(".menu-trigger"), mobile=document.querySelector(".mobile-nav");
  if(menu&&mobile){menu.addEventListener("click",()=>{const open=mobile.classList.toggle("open");menu.setAttribute("aria-expanded",open)})}
  const observer=new IntersectionObserver(entries=>entries.forEach(e=>{if(e.isIntersecting){e.target.classList.add("visible");observer.unobserve(e.target)}}),{threshold:.12});
  document.querySelectorAll(".reveal").forEach(el=>observer.observe(el));
});
