// colorUtils.js
const CalculateColor = (percentage) => {
    if (percentage === 0) {
        return 'white';
    } else if (percentage === 100) {
        return 'red';
    } else {
        const red = Math.round((percentage / 100) * 255);
        return `rgb(255, ${255-red}, ${255-red})`;
    }
};

export default CalculateColor;