import React from "react";
import { format } from "date-fns";
import Icon from "./Icon";

interface DateSelectorProps {
  dates: Date[];
  selectedDate: Date;
  onSelectDate: (date: Date) => void;
}

const DateSelector = ({
  dates,
  selectedDate,
  onSelectDate,
}: DateSelectorProps) => {
  const isSelected = (date: Date) => {
    return format(date, "yyyy-MM-dd") === format(selectedDate, "yyyy-MM-dd");
  };
  return (
    <div className="mb-6">
      <div className="flex items-center mb-3">
        <Icon name="calendar" size={20} className="mr-2" />
        <h2 className="text-lg font-medium">Select a date</h2>
      </div>
      <div className="flex flex-wrap gap-2">
        {dates.map((date, index) => (
          <button
            key={index}
            onClick={() => onSelectDate(date)}
            className={`px-4 py-2 rounded-md text-sm font-medium transition-colors
              ${
                isSelected(date)
                  ? "bg-primary-600 text-white"
                  : "bg-gray-100 text-gray-700 hover:bg-gray-200"
              }`}
          >
            <div className="text-xs">{format(date, "EEE")}</div>
            <div className="text-base font-semibold">{format(date, "d")}</div>
            <div className="text-xs">{format(date, "MMM")}</div>
          </button>
        ))}
      </div>
    </div>
  );
};

export default DateSelector;
