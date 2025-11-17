import {useState} from 'react';
import { Outlet } from 'react-router-dom';
import { NavLink, useNavigate } from "react-router-dom";
// import './Navbar.css;'
import { BsArrowLeftShort, BsPostcardHeart, BsPeopleFill } from "react-icons/bs";
import { IoHome } from "react-icons/io5";






const NavBar = ({updateUser}) => {
    const [open, setOpen] = useState(true)
    const navigate = useNavigate()


    const handleLogout = () => {
        fetch('/api/logout',{
            method:'DELETE'
        })
        .then(res => {
            if(res.ok) {
                    updateUser(null)
                    navigate('/authentication')
            }
        })
    }

    const links = [
        {to: "/", lable: "Home", icon:<IoHome size={22} />, end: true },
        {to: "/posts", lable: "Posts", icon:<BsPostcardHeart size={22} />, end: true },
        {to: "/groups", lable: "Groups", icon:<BsPeopleFill size={22} />, end: false },
    ]

    return (
        <div className="flex">
            <div 
            className={`flex flex-col justify-between bg-[#3D7E9F] h-screen p-5 pt-8 
            ${open ? "w-72" : "w-20"} duration-300 fixed`}
            >
                
                {/*Toggle button */}
                <BsArrowLeftShort className={`bg-white text-[#3498DB] text-3xl rounded-full absolute -right-3 top-9 
                border border-[#3d7e9f] cursor-pointer ${!open && "rotate-180"}`}
                onClick={() => setOpen(!open)}
                />

                {/*Nav links */} 
                <nav className="flex flex-col justify-center mt-16 space-y-6">
                    {links.map((link) => (
                        <NavLink
                            key={link.to}
                            to={link.to}
                            end={link.end}
                            className={({ isActive }) =>
                                `flex items-center gap-4 rounded-md cursor-pointer p-3 transition-all duration-200
                                ${isActive ? 
                                "bg-[#86ABBD] text-white" : "text-white hover:bg-[#357187]"
                                }`
                            }
                        >
                            <span className="text-2xl">{link.icon}</span>
                            <span className={`${!open && "hidden"} text-base font-medium`}>
                                
                            {link.lable}</span>

                        </NavLink>
                      
                ))}
                </nav>

                {/* //Logout button */}
                <button onClick={handleLogout} className="text-white hover:text-gray-200 transistion">
                    Logout
                </button>
            </div>

            {/* Render Page Content */}
            <main 
                className={`flex-1 p-8 transition-all duration-300 
                ${open ? "ml-72" : "ml-20"}`}
            >
                <Outlet />
            </main>
        </div> 
    )
}
 
export default NavBar

