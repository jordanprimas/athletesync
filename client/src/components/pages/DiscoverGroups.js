import { useState } from "react";
import GroupList from "../groups/GroupList";
import Loading from "../Loading";

const DiscoverGroups = ( {groups, user} ) => {
    const [inputSearch, setInputSearch] = useState("");
    const [sortOption, setSortOption] = useState("az")
    const [showJoinedOnly, setShowJoinedOnly] = useState(false)

    if (!groups?.length) return <Loading message="Loading" />


    const handleSearch = (e) => {
        setInputSearch(e.target.value);
    }

    let displayedGroups = groups.filter((group) =>
        group.name.toLowerCase().includes(inputSearch.trim().toLowerCase())
    );

    if (showJoinedOnly) {
        displayedGroups = displayedGroups.filter(group =>
        group.user_groups?.some(ug => ug.user_id === user.id)
        );
    }

    if (sortOption === "az") {
        displayedGroups.sort((a,b) => a.name.localeCompare(b.name));
    } else if (sortOption === "za") {
        displayedGroups.sort((a,b) => b.name.localeCompare(a.name));
    } else if (sortOption === "members") {
        displayedGroups.sort((a,b) => b.user_groups?.length - a.user_groups?.length);
    }  
    

        

     return(
        <div>
            {/* Header */}
            <div className="flex justify-between items-center">
                <div>
                <h1 className="text-2xl font-bold text-gray-900">Discover Groups 💬</h1>
                <p>Join communities that share your interests!</p>
                </div>

                {/* Add logic to create group button */}

                <button
                className="bg-[#FF7E6B] hover:bg-[#E56253] text-white font-medium px-4 py-2 rounded-lg shadow-md transition-all duration-200"
                >
                Create Group 
                </button>
            </div>
                

            {/* Search/Sort bar */}
            <div className="flex flex-col sm:flex-row justify-between items-center gap-3 mt-4">
                <input
                type="text"
                onChange={(e) => handleSearch(e)}
                placeholder="Search groups..."
                className="mt-3 sm:mt-0 px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400"
                />

                <div className="flex items-center gap-3">
                {/* Sort dropdown */}
                    <select
                        value={sortOption}
                        onChange={(e) => setSortOption(e.target.value)}
                        className="px-3 py-2 border rounded-lg text-sm focus:ring-2 focus:ring-blue-400"
                    >
                        <option value="az">Sort: A-Z</option>
                        <option value="za">Sort: Z-A</option>
                        <option value="members">Sort: Popular</option>
                    </select>

                    {/* Joined toggle */}
                    <button
                        onClick={() => setShowJoinedOnly(prev => !prev)}
                        className={`px-3 py-2 text-sm rounded-lg border transition ${
                        showJoinedOnly 
                            ? "bg-blue-100 border-blue-400 text-blue-600" 
                            : "border-gray-300 text-gray-600 hover:bg-gray-100"
                        }`}
                    >
                        {showJoinedOnly ? "Show All Groups" : "Show Joined Groups"}
                    </button>
                </div>
            </div>
            <GroupList displayedGroups={displayedGroups} />
        </div>
    )

}
export default DiscoverGroups;