import React, { useEffect, useState } from 'react';
import { AspectRatio, Column, OverflowMenu, OverflowMenuItem, Popover, PopoverContent, IconButton } from '@carbon/react';
import { Documentation } from '@carbon/pictograms-react';

export const DocumentMap = ({ rows }) => {
    const [openPopoverTable, setOpenPopoverTable] = useState([]);

    useEffect(() => {
        setOpenPopoverTable(new Array(rows.length).fill(false));
    }, [rows]);

    const displayPopoverTable = (index, open) => {
        const newOpenPopoverTable = openPopoverTable.map((item, i) => (i === index ? open : false));
        setOpenPopoverTable(newOpenPopoverTable);
    }

    return (
        <>
            {rows.length === 0 && <Column lg={3} md={2} sm={2} >
                <h3>No documents found</h3>
            </Column>}

            {rows.map((row, i) => (
                <Column key={i} lg={3} md={2} sm={2} >
                    <AspectRatio className="card" ratio="4x3">
                        <div className="card-header" >
                            <Documentation style={{ padding: "0.5rem" }} />
                            <OverflowMenu className="card-menu">
                                {/*<OverflowMenuItem itemText="Open" />*/}
                                <OverflowMenuItem hasDivider isDelete itemText="Delete" disabled />
                            </OverflowMenu>
                        </div>
                        {/* <div className="card-name">{row?.id}</div> */}
                        <div className="card-label">Chunk source: {row.metadata["source"]}</div>

                        <div className="card-label">Chunk content:</div>
                        <div className="card-description" style={{ maxHeight: "10rem" }}>{row.page_content.length > 256 ? row.page_content.substring(0, 256) + "..." : row.page_content}</div>
                    </AspectRatio>
                </Column>
            ))}
        </>
    );
};

export default DocumentMap;
