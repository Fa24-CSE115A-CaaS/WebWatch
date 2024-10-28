import { useEffect, useRef, useState } from "react";

const usePopup = () => {
  const [open, setOpen] = useState(false);
  const containerRef = useRef<HTMLDivElement>(null);

  const clickHandler = (e: MouseEvent) => {
    if (!containerRef.current?.contains(e.target as Node)) {
      setOpen(false);
    }
  };

  useEffect(() => {
    window.addEventListener("click", clickHandler, { capture: true });

    return () => {
      window.removeEventListener("click", clickHandler, { capture: true });
    };
  });

  return { open, setOpen, containerRef };
};

export default usePopup;
