$("#submitColor").click(function() {
    const hexColor = colorPicker.color.hexString;
    $.post('/setColor', { color: hexColor }, function(response) {
        $('body').css('background-color', response.profileColor);
        const invertedColor = invertColor(response.profileColor);
        $('body').css('color', invertedColor);
    });
});

function invertColor(hex) {
    const r = 255 - parseInt(hex.slice(1, 3), 16);
    const g = 255 - parseInt(hex.slice(3, 5), 16);
    const b = 255 - parseInt(hex.slice(5, 7), 16);
    return `#${((1 << 24) + (r << 16) + (g << 8) + b).toString(16).slice(1).toUpperCase()}`;
}
