import { useState } from "react";

function App() {
  const [count, setCount] = useState(0);

  return (
    <button
      className="mx-auto my-3 block cursor-pointer rounded-md bg-red-500 p-5 text-lg text-white
        transition-all duration-100 ease-out hover:bg-red-700"
      onClick={() => setCount((count) => count + 1)}
    >
      count is {count}
    </button>
  );
}

export default App;
