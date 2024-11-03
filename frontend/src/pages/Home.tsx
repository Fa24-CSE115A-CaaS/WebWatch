import React from 'react';

const Home = () => {
  return (
    <div className="min-h-screen bg-primary flex flex-col items-center justify-start text-center p-4 text-white">
      <header className="mb-8 mt-16">
        <h1 className="text-5xl font-bold text-accent mb-4">WebWatch</h1>
        <p className="text-xl text-white">Keep track of your favorite websites effortlessly</p>
      </header>
      <main className="w-full max-w-4xl bg-secondary rounded-lg shadow-lg p-8 border-solid border-border border-2">
        <section className="mb-8">
          <h2 className="text-3xl font-semibold text-accent mb-4">What We Do</h2>
          <p className="text-lg text-white">
            Our app allows you to monitor changes on any web page. Get notified instantly when something changes, so you never miss an update.
          </p>
        </section>
        <section className="mb-8">
          <h2 className="text-3xl font-semibold text-accent mb-4">Features</h2>
          <ul className="list-disc list-inside text-center text-lg text-white">
            <li>Real-time monitoring of web pages</li>
            <li>Customizable alert settings</li>
            <li>User-friendly interface</li>
          </ul>
        </section>
        <section>
          <h2 className="text-3xl font-semibold text-accent mb-4">Get Started</h2>
          <p className="text-lg text-white mb-4">
            Sign up today and start monitoring your favorite websites with ease.
          </p>
          <div className="flex justify-center space-x-4">
            <button className="mt-4 rounded-lg bg-accent py-2 px-10 text-text-contrast hover:bg-accent-hover w-40">
              Sign Up
            </button>
            <button className="mt-4 rounded-lg bg-accent py-2 px-10 text-text-contrast hover:bg-accent-hover w-40">
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
