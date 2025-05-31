import React, { useState } from "react";
import Link from "next/link";
import Icon from "./Icon";

const Navbar = () => {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  return (
    <header className="bg-white shadow-sm">
      <nav className="container mx-auto px-4 py-4 flex items-center justify-between">
        {" "}
        {/* Logo */}
        <Link href="/" className="flex items-center space-x-2">
          <img
            src="/icons/logo.svg"
            alt="MovieObserver Logo"
            className="h-8 w-8"
          />
          <span className="text-xl font-bold text-primary-700">
            MovieObserver
          </span>
        </Link>
        {/* Desktop Navigation */}
        <div className="hidden md:flex space-x-8">
          <Link
            href="/"
            className="text-gray-600 hover:text-primary-700 transition-colors"
          >
            Home
          </Link>
          <Link
            href="/about"
            className="text-gray-600 hover:text-primary-700 transition-colors"
          >
            About
          </Link>
          <Link
            href="/theaters"
            className="text-gray-600 hover:text-primary-700 transition-colors"
          >
            Theaters
          </Link>
        </div>
        {/* Mobile Menu Button */}
        <div className="md:hidden">
          <button
            type="button"
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="text-gray-600 hover:text-primary-700 focus:outline-none"
          >
            {" "}
            {mobileMenuOpen ? (
              <Icon name="close" size={24} />
            ) : (
              <Icon name="menu" size={24} />
            )}
          </button>
        </div>
      </nav>

      {/* Mobile Menu */}
      {mobileMenuOpen && (
        <div className="md:hidden bg-white border-t border-gray-100">
          <div className="container mx-auto px-4 py-2 space-y-2">
            <Link
              href="/"
              onClick={() => setMobileMenuOpen(false)}
              className="block py-2 text-gray-600 hover:text-primary-700"
            >
              Home
            </Link>
            <Link
              href="/about"
              onClick={() => setMobileMenuOpen(false)}
              className="block py-2 text-gray-600 hover:text-primary-700"
            >
              About
            </Link>
            <Link
              href="/theaters"
              onClick={() => setMobileMenuOpen(false)}
              className="block py-2 text-gray-600 hover:text-primary-700"
            >
              Theaters
            </Link>
          </div>
        </div>
      )}
    </header>
  );
};

export default Navbar;
