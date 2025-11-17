import { useState } from "react";

import { ChevronDown, ChevronUp } from "lucide-react"
import GroupCard from "./GroupCard";


const GroupList = ({ displayedGroups }) => {
 
  if (!Array.isArray(displayedGroups) || displayedGroups.length === 0) {
    return <div className="text-gray-500 p-4">No groups available</div>;
  }

  const groupElementList = displayedGroups.map((group) => 
    <GroupCard key={group.id} group={group} />
  );

  

  return (
    <div className="grid grid-cols-[repeat(auto-fit,minmax(300px,400px))] gap-6">
      {groupElementList}
    </div>
  );
};

export default GroupList;
