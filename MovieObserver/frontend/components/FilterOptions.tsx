import React from 'react';

interface FilterOptionsProps {
  showOriginalOnly: boolean;
  setShowOriginalOnly: (show: boolean) => void;
}

const FilterOptions = ({ showOriginalOnly, setShowOriginalOnly }: FilterOptionsProps) => {
  return (
    <div className="bg-gray-50 p-4 rounded-lg mb-6">
      <h2 className="text-lg font-medium mb-2">Filter Options</h2>
      
      <div className="flex items-center">
        <input
          id="original-language"
          type="checkbox"
          checked={showOriginalOnly}
          onChange={(e) => setShowOriginalOnly(e.target.checked)}
          className="h-5 w-5 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
        />
        <label htmlFor="original-language" className="ml-2 text-gray-700">
          Show only original language screenings
        </label>
      </div>
      
      {/* Additional filters can be added here */}
    </div>
  );
};

export default FilterOptions;
