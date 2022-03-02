// SPDX-FileCopyrightText: 2022 easyDiffraction contributors <support@easydiffraction.org>
// SPDX-License-Identifier: BSD-3-Clause
// © 2021-2022 Contributors to the easyDiffraction project <https://github.com/easyScience/easyDiffractionApp>

function highlightCifSyntax(str)
{
    return str
        .replace(/data_\w+/ig, `<font color=${EaStyle.Colors.red}>$&</font>`)          // colorize datablock, e.g., "data_Fe3O4"
        .replace(/loop_/ig, `<font color=${EaStyle.Colors.grey}>loop_</font>`)         // colorize "loop_"
        .replace(/(_[\w.-]+) /ig, `<font color=${EaStyle.Colors.blue}>$1</font> `)     // colorize individual keys (with space at the end), e.g., "_setup_wavelength"
        .replace(/(_[\w.-]+)\n/ig, `<font color=${EaStyle.Colors.green}>$1</font>\n`)  // colorize keys inside loops (with new line at the end), e.g., "_phase_label"
        .replace(/(\r\n|\r|\n)/ig, "<br />")                                           // change newline and carriage return escape sequences to html format
}

function removeCifSyntaxHighlighting(html)
{
    // regex tester: https://regexr.com/
    return html
        .replace(/(\r\n|\r|\n)/ig, "")    // remove newline and carriage return escape sequences
        .replace(/<br \/>/ig, "\n")       // convert newline from html format to escape sequences
        .replace(/<style.+style>/ig, "")  // remove html style group
        .replace(/<\/?[^>]+>/ig, "")      // remove html tags
}
