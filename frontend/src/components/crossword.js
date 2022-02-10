import React from 'react';
import Cell from './cell';
import '../styles/Crossword.css'

const Crossword = ({ check, grid, reset, setReset}) => {

    const renderRow = (row) => {
        return (row.map(cell => { return (<td key={cell.cords}>{<Cell cell={cell} check={check} reset={reset} setReset={setReset}></Cell>}</td>) }))
    }

    return <table id='crossword'>
        <tbody>
            {grid.length > 0 ? grid.map((row, i) => { return (<tr key={i}>{renderRow(row)}</tr>) }
            ) : console.log("VIGA")}
        </tbody>
    </table>

}

export default Crossword