import Link from "next/link";

export default function SideBar() {
  return (
    <div className="w-64 h-screen bg-gray-800 text-white flex flex-col fixed">
      <div className="p-4 text-xl font-bold">Sidebar</div>
      <nav className="flex-1">
        <ul className="space-y-2">
          <li>
            <Link
              href="/indeed"
              className="block px-4 py-2 hover:bg-gray-700"
            >
              Indeed
            </Link>
          </li>
          <li>
            <Link
              href="/linkedin"
              className="block px-4 py-2 hover:bg-gray-700"
            >
              LinkedIn
            </Link>
          </li>
        </ul>
      </nav>
    </div>
  );
}
