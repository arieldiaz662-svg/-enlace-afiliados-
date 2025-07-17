import React from "react";
import "./App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { LanguageProvider } from "./context/LanguageContext";
import Header from "./components/Layout/Header";
import Footer from "./components/Layout/Footer";
import HomePage from "./components/Home/HomePage";

function App() {
  return (
    <LanguageProvider>
      <div className="App">
        <BrowserRouter>
          <Header />
          <main>
            <Routes>
              <Route path="/" element={<HomePage />} />
            </Routes>
          </main>
          <Footer />
        </BrowserRouter>
      </div>
    </LanguageProvider>
  );
}

export default App;
