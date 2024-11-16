import useTheme from "../hooks/useTheme";

function Guide() {
  const { changeTheme } = useTheme();

  const btnStyles =
    "text-text font-main m-3 block w-52 rounded-md px-3 py-2 font-medium border-[1px] border-border";
  return (
    <div className="h-screen w-screen bg-background p-5">
      <div className="mx-auto w-min">
        <button className={`${btnStyles} bg-primary`}>Primary</button>
        <button className={`${btnStyles} bg-secondary`}>Secondary</button>
        <button className={`${btnStyles} bg-accent text-text-contrast`}>
          Accent
        </button>
        <button className={`${btnStyles} bg-accent-hover text-text-contrast`}>
          Accent Hover
        </button>
        <button className={`${btnStyles} bg-border`}>Border</button>
        <button className={`${btnStyles} bg-error`}>Error</button>
        <button className={`${btnStyles} bg-info text-text-contrast`}>
          Info
        </button>
        <button className={`${btnStyles} bg-text text-text-contrast`}>
          Text
        </button>
        <button className={`${btnStyles} bg-text-contrast`}>
          Text Contrast
        </button>
        <button className={`${btnStyles} bg-primary`} onClick={changeTheme}>
          Change Theme
        </button>
      </div>
    </div>
  );
}

export default Guide;
