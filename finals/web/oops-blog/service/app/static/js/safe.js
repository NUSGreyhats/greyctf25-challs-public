const observer = new MutationObserver((mutationsList) => {
  for (const mutation of mutationsList) {
    if (mutation.type === "childList" && mutation.addedNodes.length > 0) {
      mutation.addedNodes.forEach((node) => {
        if (node.nodeType === Node.ELEMENT_NODE) {
            if(node.classList.contains("safe")){
                console.log("Executing", node);
                eval(node.textContent);
            }
            for(const safeElement of node.getElementsByClassName("safe")){
                console.log("Executing", safeElement);
                eval(safeElement.textContent);
            }
        }
      });
    }
  }
});

observer.observe(document.body, { childList: true, subtree: true });