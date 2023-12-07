(function () {
    "use strict";

    const sidebar = document.querySelector('.sidebar');
    const sidebarToggles = document.querySelectorAll('#sidebarToggle, #sidebarToggleTop');
    const fixedNavigation = document.querySelector('body.fixed-nav .sidebar');
    const scrollToTop = document.querySelector('.scroll-to-top');

    function handleScrollToTopDisplay() {
        scrollToTop.style.display = window.scrollY > 100 ? 'block' : 'none';
    }

    function handleSidebarToggleClick() {
        document.body.classList.toggle('sidebar-toggled');
        sidebar.classList.toggle('toggled');
        if (sidebar.classList.contains('toggled')) hideSidebarCollapses();
    }

    function handleWindowResize() {
        if (window.innerWidth < 768) hideSidebarCollapses();
    }

    function handleFixedNavigationWheel(e) {
        if (window.innerWidth > 768) {
            e.preventDefault();
            fixedNavigation.scrollTop += (e.deltaY < 0 ? -1 : 1) * 30;
        }
    }

    function hideSidebarCollapses() {
        const sidebarCollapseList = Array.from(document.querySelectorAll('.sidebar .collapse')).map(collapseEl => new bootstrap.Collapse(collapseEl, {toggle: false}));
        sidebarCollapseList.forEach(bsCollapse => bsCollapse.hide());
    }

    if (sidebar) {
        sidebarToggles.forEach(sidebarToggle => sidebarToggle.addEventListener('click', handleSidebarToggleClick));
        window.addEventListener('resize', handleWindowResize);
    }

    if (fixedNavigation) {
        fixedNavigation.addEventListener('wheel', handleFixedNavigationWheel);
    }

    if (scrollToTop) {
        window.addEventListener('scroll', handleScrollToTopDisplay);
    }

})()