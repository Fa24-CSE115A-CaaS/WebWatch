import { Link } from "react-router-dom";

const Home = () => {
  return (
    <div
      className="flex min-h-screen flex-col items-center justify-start bg-primary p-4 text-center
        text-text"
    >
      <header className="mb-8 mt-16">
        <h1 className="mb-4 text-5xl font-bold text-accent">WebWatch</h1>
        <p className="text-xl text-text">
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
          <p className="text-lg text-text">
            Our app allows you to monitor changes on any web page. Get notified
            instantly when something changes, so you never miss an update.
          </p>
        </section>
        <section className="mb-8">
          <h2 className="mb-4 text-3xl font-semibold text-accent">Features</h2>
          <ul className="list-inside list-disc text-center text-lg text-text">
            <li>Real-time monitoring of web pages</li>
            <li>Customizable alert settings</li>
            <li>User-friendly interface</li>
          </ul>
        </section>
        <section>
          <h2 className="mb-4 text-3xl font-semibold text-accent">
            Get Started
          </h2>
          <p className="mb-4 text-lg text-text">
            Sign up today and start monitoring your favorite websites with ease.
          </p>
          <div className="flex justify-center space-x-4">
            <Link to="/auth">
              <button
                className="mt-4 w-40 rounded-lg bg-accent px-10 py-2 text-text-contrast
                  hover:bg-accent-hover"
              >
                Login
              </button>
            </Link>
            <Link to="/auth#register">
              <button
                className="mt-4 w-40 rounded-lg bg-accent px-10 py-2 text-text-contrast
                  hover:bg-accent-hover"
              >
                Register
              </button>
            </Link>
          </div>
        </section>
      </main>
      <footer className="mt-8 text-text">
        &copy; {new Date().getFullYear()} WebWatch. All rights reserved.
      </footer>
    </div>
  );
};

export default Home;
