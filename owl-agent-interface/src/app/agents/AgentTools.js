import { DropdownSkeleton, MultiSelect } from "@carbon/react";
import React, { useEffect, useState } from "react";
import { Octokit } from '@octokit/core';

const octokitClient = new Octokit({});

const AgentTools = ({ backendBaseAPI, toolSelectedItems, setToolSelectedItems, setError }) => {
    const [loading, setLoading] = useState(true);
    const [dropdownItemsTools, setDropdownItemsTools] = useState([]);

    useEffect(() => {
        // Preload tools
        async function getTools() {
            try {
                const res = await octokitClient.request(`GET ${backendBaseAPI}a/tools`);
                if (res.status === 200) {
                    const items = res.data.map(tool => (tool.tool_id));
                    setDropdownItemsTools(items);
                } else {
                    setError('Error obtaining tool data (' + res.status + ')');
                    console.error('Error obtaining tool data ', res);
                }
            } catch (error) {
                setError('Error obtaining tool data:' + error.message);
                console.error('Error obtaining tool data:' + error);
            }
        }

        setLoading(true);
        try {
            getTools();
        } finally {
            setLoading(false);
        }
    }, []);

    return (
        <div>
            {loading && (<DropdownSkeleton />)}
            {!loading && (<MultiSelect id="multi-select-tools"
                key={toolSelectedItems.selectedItems.join(",")}
                label="Tools"
                titleText="Tools"
                items={dropdownItemsTools}
                initialSelectedItems={toolSelectedItems.selectedItems}
                onChange={(selection) => setToolSelectedItems(selection)}
                selectionFeedback="top-after-reopen" />)
            }
            <div style={{ display: 'flex', alignItems: 'center', marginTop: '1rem', height: '3rem' }} />
        </div>
    );
};

export default AgentTools;