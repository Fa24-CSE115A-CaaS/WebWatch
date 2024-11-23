// Framer
import { motion, AnimatePresence } from "framer-motion";
// Types
import { NotificationsComponent } from "./types";
// Icons
import { MdOutlineCancel } from "react-icons/md";
import { FaRegCheckCircle } from "react-icons/fa";
import { AiOutlineInfoCircle } from "react-icons/ai";
import { PiWarningCircleBold } from "react-icons/pi";

const notificationVariant = {
  visible: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.2, ease: "easeOut", type: "spring" },
  },
  hidden: {
    opacity: 0,
    y: -20,
    transition: { duration: 0.1, ease: "easeOut" },
  },
};

const Notifications: NotificationsComponent = ({ notifications }) => {
  return (
    <div className="fixed inset-0 top-5 mx-auto flex w-max flex-col items-center">
      <AnimatePresence>
        {notifications.reverse().map(({ id, message, type }) => (
          <motion.div
            key={id}
            variants={notificationVariant}
            initial="hidden"
            animate="visible"
            exit="hidden"
            transition={{ layout: { duration: 0.2, ease: "easeOut" } }}
            className="mb-2 flex w-max items-center gap-3 rounded-full border-[1px] border-border
              bg-primary py-2 pl-4 pr-5 text-text shadow-lg"
            layout
          >
            {type === "ERROR" && (
              <MdOutlineCancel className="h-5 w-5 text-error" />
            )}
            {type === "SUCCESS" && (
              <FaRegCheckCircle className="h-5 w-5 text-success" />
            )}
            {type === "INFO" && (
              <AiOutlineInfoCircle className="h-5 w-5 text-info" />
            )}
            {type === "WARNING" && (
              <PiWarningCircleBold className="h-5 w-5 text-warning" />
            )}
            <p className="text-sm">{message}</p>
          </motion.div>
        ))}
      </AnimatePresence>
    </div>
  );
};

export default Notifications;
