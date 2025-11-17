import { Link } from "react-router-dom";

const GroupCard = ({ group }) => {

    return(
      <div className="flex flex-col gap-6">
    
          <div

            className=" bg-white rounded-xl shadow-md border border-gray-200 overflow-hidden transition transform hover:shadow-lg duration-200"
          >
            {/* Cover Image */}
            <div className="h-40 w-full bg-gray-200">
              <img
                src={group.cover_image || "https://via.placeholder.com/600x200?text=Group+Cover"}
                alt={`${group.name} cover`}
                className="h-full w-full object-cover"
              />
            </div>

            {/* Group Cards */}
            <div className="p-5 flex flex-col gap-3">
              <div className="flex justify-between items-start">
                <h2 className="text-xl font-semibold text-[#3D7E9F]">{group.name}</h2>
              </div>

              {group.description && (
                <p className="text-gray-600 text-sm line-clamp-2">
                  {group.description}
                </p>
              )}

              <Link
                to={`/groups/${group.id}`}
                className="px-4 py-2 rounded-lg bg-[#FF7E6B] text-white font-medium hover:bg-[#E56253] transition duration-200"
              >
                Visit Group
              </Link>
              
            </div>
          </div>
      

        </div>
    )

}
export default GroupCard;