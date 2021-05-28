<script lang="typescript">
  import type { Orientation } from "./util/types";
  import { globalViewConfig } from "./state/view-config";

  export let id: Orientation;

  $: isHidden = id === "center" ? !$globalViewConfig.showCenter : false;
</script>

<div id="{id}-view-config" class="view-config {id} {isHidden ? "hidden" : ""}"></div>

<style>
  .view-config {
    border: none;
    box-sizing: border-box;
    width: 100%;
    background: black;
    color: white;
    height: 23px;
  }
  .view-config.center {
    border-left: 1px solid white;
    border-right: 1px solid white;
  }
  .view-config.hidden {
    width: 0;
    overflow: hidden;
  }
</style>