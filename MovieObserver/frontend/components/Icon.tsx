import React from 'react';

type IconProps = {
  name: string;
  size?: number;
  color?: string;
  className?: string;
};

/**
 * Icon component for displaying SVG icons
 * 
 * @param {string} name - The name of the icon (filename without extension)
 * @param {number} size - The size of the icon in pixels
 * @param {string} color - CSS color value to override the icon color
 * @param {string} className - Additional CSS classes
 */
const Icon: React.FC<IconProps> = ({ name, size = 24, color, className = '' }) => {
  return (
    <div 
      className={`inline-flex items-center justify-center ${className}`}
      style={{ 
        width: size, 
        height: size,
      }}
    >
      <img 
        src={`/icons/${name}.svg`} 
        alt={`${name} icon`} 
        width={size} 
        height={size}
        style={color ? { filter: `${getColorFilter(color)}` } : {}}
      />
    </div>
  );
};

/**
 * Converts a hex color to a CSS filter to colorize the SVG
 * This is a simple implementation and might not work perfectly for all colors
 */
const getColorFilter = (hexColor: string): string => {
  // For simplicity, we'll just use brightness and contrast filters
  // A more accurate approach would use matrix filters
  if (hexColor.startsWith('#')) {
    // Simple approach - works okay for basic recoloring
    return 'brightness(0) saturate(100%) ' + 
           `invert(${getColorBrightness(hexColor)}) ` + 
           `sepia(${getColorSaturation(hexColor)}) ` + 
           `saturate(${getColorIntensity(hexColor)}) ` + 
           `hue-rotate(${getColorHue(hexColor)}deg)`;
  }
  return '';
};

// Helper functions for color conversion
// These are simplified and not accurate for all colors
const getColorBrightness = (hex: string): number => {
  const r = parseInt(hex.slice(1, 3), 16) / 255;
  const g = parseInt(hex.slice(3, 5), 16) / 255;
  const b = parseInt(hex.slice(5, 7), 16) / 255;
  return Math.max(r, g, b);
};

const getColorSaturation = (hex: string): number => {
  const r = parseInt(hex.slice(1, 3), 16) / 255;
  const g = parseInt(hex.slice(3, 5), 16) / 255;
  const b = parseInt(hex.slice(5, 7), 16) / 255;
  const max = Math.max(r, g, b);
  const min = Math.min(r, g, b);
  return max === 0 ? 0 : (max - min) / max;
};

const getColorIntensity = (hex: string): number => {
  return 1 + Math.random() * 10; // Simplified
};

const getColorHue = (hex: string): number => {
  const r = parseInt(hex.slice(1, 3), 16) / 255;
  const g = parseInt(hex.slice(3, 5), 16) / 255;
  const b = parseInt(hex.slice(5, 7), 16) / 255;
  
  const max = Math.max(r, g, b);
  const min = Math.min(r, g, b);
  
  let h = 0;
  
  if (max === min) {
    h = 0;
  } else if (max === r) {
    h = 60 * ((g - b) / (max - min));
  } else if (max === g) {
    h = 60 * (2 + (b - r) / (max - min));
  } else {
    h = 60 * (4 + (r - g) / (max - min));
  }
  
  if (h < 0) h += 360;
  return h;
};

export default Icon;
