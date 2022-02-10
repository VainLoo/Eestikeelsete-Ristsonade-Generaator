import React, { useState, useEffect } from 'react';
import { InputText } from 'primereact/inputtext';
import '../styles/Cell.css';


const Cell = ({ cell, check, reset, setReset}) => {

    const [value, setValue] = useState('');
    const [truevalue] = useState(cell.contents);

    useEffect(() => {
        if (reset) setValue('');
        setReset(false);
    }, [reset]);

    return (
        <div>
            {cell.contents !== '#' ?
                <div className='box'>
                    <i className="cornerNumber p-component">{cell.clueNumber}</i>
                    {check ? value === truevalue ? <InputText className='cell rightCell border-noround' maxLength="1" id="cell" value={value} onChange={(e) => setValue(e.target.value.toUpperCase())} keyfilter={/^[a-zöäüõA-ZÖAÖÜ ]$/} data-truevalue={truevalue} />
                        : <InputText className='cell wrongCell border-noround' maxLength="1" id="cell" value={value} onChange={(e) => setValue(e.target.value.toUpperCase())} keyfilter={/^[a-zöäüõA-ZÖAÖÜ ]$/} data-truevalue={truevalue} />
                        : <InputText className='cell border-noround' maxLength="1" id="cell" value={value} onChange={(e) => setValue(e.target.value.toUpperCase())} keyfilter={/^[a-zöäüõA-ZÖAÖÜ ]$/} data-truevalue={truevalue} />
                    }

                </div>
                : <div className='cell bg-black-alpha-90 border-noround'></div>
            }
        </div>
    )

}

export default Cell