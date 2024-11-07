const Home = () => {
  return (
    <div
      className="flex min-h-screen flex-col items-center justify-start bg-primary p-4 text-center
        text-white"
    >
      <header className="mb-8 mt-16">
        <h1 className="mb-4 text-5xl font-bold text-accent">WebWatch</h1>
        <p className="text-xl text-white">
          Keep track of your favorite websites effortlessly
        </p>
      </header>
      <main
        className="w-full max-w-4xl rounded-lg border-2 border-solid border-border bg-secondary p-8
          shadow-lg"
      >
        <section className="mb-8">
          <h2 className="mb-4 text-3xl font-semibold text-accent">
            What We Do
          </h2>
          <p className="text-lg text-white">
            Our app allows you to monitor changes on any web page. Get notified
            instantly when something changes, so you never miss an update.
          </p>
        </section>
        <section className="mb-8">
          <h2 className="mb-4 text-3xl font-semibold text-accent">Features</h2>
          <ul className="list-inside list-disc text-center text-lg text-white">
            <li>Real-time monitoring of web pages</li>
            <li>Customizable alert settings</li>
            <li>User-friendly interface</li>
          </ul>
        </section>
        <section>
          <h2 className="mb-4 text-3xl font-semibold text-accent">
            Get Started
          </h2>
          <p className="mb-4 text-lg text-white">
            Sign up today and start monitoring your favorite websites with ease.
          </p>
          <div className="flex justify-center space-x-4">
            <button
              className="mt-4 w-40 rounded-lg bg-accent px-10 py-2 text-text-contrast
                hover:bg-accent-hover"
            >
              Sign Up
            </button>
            <button
              className="mt-4 w-40 rounded-lg bg-accent px-10 py-2 text-text-contrast
                hover:bg-accent-hover"
            >
              Login
            </button>
          </div>
        </section>
      </main>
      <footer className="mt-8 text-white">
        &copy; {new Date().getFullYear()} WebWatch. All rights reserved.
      </footer>
    </div>
  );
};

export default Home;
