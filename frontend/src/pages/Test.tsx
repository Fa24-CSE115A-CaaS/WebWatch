import { useState, useEffect } from "react";

const Test = () => {
  const [currentTime, setCurrentTime] = useState(new Date());

  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentTime(new Date());
    }, 1000);

    return () => clearInterval(timer);
  }, []);

  return (
    <div
      className="mt-4 flex min-h-screen flex-col items-center justify-start p-4 text-center
        text-text"
    >
      <main
        className="w-full max-w-4xl rounded-lg border-2 border-solid border-border bg-secondary p-8
          shadow-lg"
      >
        <section className="mb-8">
          <h2 className="mb-4 text-3xl font-semibold text-accent">
            Verify your WebWatching setup
          </h2>
          <p className="text-lg text-text">
            Use this clock page as an example to get started with WebWatching;
            create a new task to watch this URL and ensure your notification
            methods and intervals are set up correctly.
          </p>
        </section>
        <p className="text-2xl text-accent">
          {currentTime.toLocaleString()}
        </p>
      </main>
    </div>
  );
};

export default Test;
