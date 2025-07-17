import React from 'react';
import { useLanguage } from '../../context/LanguageContext';
import { Leaf, Mail, Phone, MapPin, Facebook, Instagram, Twitter } from 'lucide-react';

const Footer = () => {
  const { t } = useLanguage();

  return (
    <footer className="bg-gradient-to-r from-green-800 to-emerald-900 text-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* Logo and Description */}
          <div className="col-span-1 md:col-span-2">
            <div className="flex items-center space-x-2 mb-4">
              <div className="bg-green-600 p-2 rounded-full">
                <Leaf className="h-6 w-6 text-white" />
              </div>
              <h3 className="text-xl font-bold">{t('title')}</h3>
            </div>
            <p className="text-green-200 mb-4 max-w-md">
              {t('subtitle')}
            </p>
            <div className="flex space-x-4">
              <a href="#" className="text-green-200 hover:text-white transition-colors duration-200">
                <Facebook className="h-5 w-5" />
              </a>
              <a href="#" className="text-green-200 hover:text-white transition-colors duration-200">
                <Instagram className="h-5 w-5" />
              </a>
              <a href="#" className="text-green-200 hover:text-white transition-colors duration-200">
                <Twitter className="h-5 w-5" />
              </a>
            </div>
          </div>

          {/* Quick Links */}
          <div>
            <h4 className="font-semibold mb-4 text-green-100">Enlaces Rápidos</h4>
            <ul className="space-y-2">
              <li>
                <a href="#cepillos-bambu" className="text-green-200 hover:text-white transition-colors duration-200">
                  Cepillos de Bambú
                </a>
              </li>
              <li>
                <a href="#champu-solido" className="text-green-200 hover:text-white transition-colors duration-200">
                  Champús Sólidos
                </a>
              </li>
              <li>
                <a href="#cuidado-facial" className="text-green-200 hover:text-white transition-colors duration-200">
                  Cuidado Facial
                </a>
              </li>
              <li>
                <a href="#kits-sostenibles" className="text-green-200 hover:text-white transition-colors duration-200">
                  Kits Sostenibles
                </a>
              </li>
              <li>
                <a href="#blog" className="text-green-200 hover:text-white transition-colors duration-200">
                  {t('blog')}
                </a>
              </li>
            </ul>
          </div>

          {/* Contact Info */}
          <div>
            <h4 className="font-semibold mb-4 text-green-100">Contacto</h4>
            <div className="space-y-2">
              <div className="flex items-center space-x-2">
                <Mail className="h-4 w-4 text-green-400" />
                <span className="text-green-200">info@bambugoods.com</span>
              </div>
              <div className="flex items-center space-x-2">
                <Phone className="h-4 w-4 text-green-400" />
                <span className="text-green-200">+34 900 123 456</span>
              </div>
              <div className="flex items-center space-x-2">
                <MapPin className="h-4 w-4 text-green-400" />
                <span className="text-green-200">Madrid, España</span>
              </div>
            </div>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="border-t border-green-700 mt-8 pt-8 text-center">
          <p className="text-green-200 text-sm">
            &copy; 2025 {t('title')}. {t('copyright')}
          </p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;